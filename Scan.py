import socket
import sys
import pyfiglet
from datetime import datetime
import os
import threading
from queue import Queue

#os.system('cls')  # clear Shell
os.system('clear')
banner = pyfiglet.figlet_format("Folcoxx SCANNER")
print(banner)
remoteServer = input("Enter a remote host or IP to scan: ")
PortRange = input("Port range (1,1024): ")
print("-" * 50)
print_lock = threading.Lock()

def ipv4addr(remoteServer):   # Check IPv4
    try:
        socket.inet_pton(socket.AF_INET, remoteServer)
    except AttributeError:
        try:
            socket.inet_aton(remoteServer)
        except socket.error:
            return False
    except socket.error:
        return False
    return True

def ipv6addr(remoteServer): #Check IPv6
    try:
        socket.inet_pton(socket.AF_INET6, remoteServer)
    except socket.error:
        return False
    return True

if (ipv4addr(remoteServer)==False) and (ipv6addr(remoteServer)==False): #If it's Name DNS resolve
        remoteServerIP = socket.gethostbyname(remoteServer)
        print("[+] Scanning", remoteServerIP)
else:   # else Inverse resolve
    remoteServerIP = remoteServer
    try:
        remoteHostname = socket.gethostbyaddr(remoteServerIP)
        print("[+] Scanning", remoteHostname)
    except socket.error:
        print("Pas de hostname")

dt = datetime.now() #Check Start time

def scan4(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect((remoteServerIP, port))
        with print_lock:
            print("[+] Port",str(port),":  Open")
        con.close()
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass

def scan6(port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        con = sock.connect((remoteServerIP, port))
        with print_lock:
            print("[+] Port",str(port),":  Open")
        con.close()
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass

def threader():
    while True:
        if ipv4addr(remoteServerIP):
            jobs = q.get()
            scan4(jobs)
            q.task_done()
        elif ipv6addr(remoteServerIP):
            jobs = q.get()
            scan6(jobs)
            q.task_done()

q = Queue()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

if PortRange.find(',') != -1:
    PortRange1, PortRange2 = PortRange.split(",")
    for jobs in range(int(PortRange1), int(PortRange2) + 1):
        q.put(jobs)
    q.join()
else:
    port = int(PortRange)
    q.put(port)
    q.join()

fd = datetime.now()   #Check End Time
Timett = fd - dt
print("-" * 50)
print("Total Time of Scan", Timett)