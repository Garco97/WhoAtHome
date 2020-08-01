import sys
import subprocess
import os
import decouple
import ipaddress
import threading
import time
IP_NETWORK = ipaddress.ip_address('192.168.1.1')

ip_net = ipaddress.ip_network('192.168.1.0/24')
# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE
def run(i):
    output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
    if "100% perdidos" in str(output):
        pass
        #print(str(all_hosts[i]), "is Offline")
    else:
        print(str(all_hosts[i]), "is Online")
# Get all hosts on that network
all_hosts = list(ip_net.hosts())
for i in range(len(all_hosts)):
    #time.sleep(0.1)
    t = threading.Thread(target=run, args=(i,))
    t.start()
    

