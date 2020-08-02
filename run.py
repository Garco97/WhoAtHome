import subprocess
import smtplib
import ipaddress
import threading
import time
import json
def run(i):
    output,error = subprocess.Popen(['ping','-c','3', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()
    if "100% packet loss" not in str(output):
        ips.append(str(all_hosts[i]))

if __name__ == "__main__":
    minutes = 10
    ip_net = ipaddress.ip_network('192.168.1.0/24')
    ips = []
    old_ips = []
    configuration = json.load(open("configuration.json"))
    all_hosts = list(ip_net.hosts())
    while(True):
        threads = []
        connected = []
        disconnected = []
        for i in range(len(all_hosts)):
            #time.sleep(0.1)
            t = threading.Thread(target=run, args=(i,))
            threads.append(t)
            t.start()
        for i in threads:
            i.join()
        for i in ips:
            if i not in old_ips:
                connected.append(i)
        for i in old_ips:
            if i not in ips:
                disconnected.append(i)
        if connected or disconnected:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            email = 'dgarciacosio@gmail.com'
            server.login(email,configuration["password"])
            subject = "Nuevas conexiones en casa" 
            body = "Se han conectado las siguientes direcciones IP:\n" + '\n'.join(connected)
            body += "\nSe han desconectado las siguientes direcciones IP:\n" + '\n'.join(disconnected)
            msg = f'Subject:{subject}\n\n{body}'
            server.sendmail(
                email,
                email,
                msg
            )
            server.quit()
        old_ips = ips
        ips = []
        time.sleep(60*minutes)

