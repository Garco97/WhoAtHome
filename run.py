import subprocess
import smtplib
import ipaddress
import threading
import time
import json
from types import SimpleNamespace

def run(i,user):
    output = subprocess.Popen(['ping','-c','3', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()[0]
    if "100% packet loss" not in str(output):
        ips.append(user)

def read_configuration():
    configuration = json.load(open("configuration.json"))
    configuration = SimpleNamespace(**configuration)
    return configuration
def read_users():
    users = json.load(open("users.json"))
    users = [SimpleNamespace(**user) for user in users]
    return users
if __name__ == "__main__":
    configuration = read_configuration()
    ip_net = ipaddress.ip_network(configuration.network)
    ips, old_ips = [], []
    all_hosts = list(ip_net.hosts())[configuration.first_ip - 1:configuration.last_ip - 1]
    while(True):
        threads,connected,disconnected = [], [], []
        users = read_users()
        for ip in range(len(all_hosts)):
            user = [user for user in users if user.ip == str(all_hosts[ip])[-3:]]
            if user: 
                t = threading.Thread(target=run, args=(ip,user[0],))
                threads.append(t)
                t.start()
        for thread in threads:thread.join()
        connected = [ip for ip in ips if ip not in old_ips]
        disconnected = [ip for ip in old_ips if ip not in ips]
        if connected or disconnected:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(configuration.email,configuration.password)
            body = "\n".join([user.name + configuration.arrive for user in connected])
            body += "\n" + "\n".join([user.name + configuration.leave for user in disconnected])          
            msg = f'Subject:{configuration.subject}\n\n{body}'
            emails = [user.email for user in users if user.active]
            if emails:
                server.sendmail(
                        configuration.email,
                        emails,
                        msg
                    )
            server.quit()
        old_ips = ips
        ips = []
        time.sleep(60*configuration.refresh)
