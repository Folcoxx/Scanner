import socket
import sys
import pyfiglet
from datetime import datetime
import os


#os.system('cls')  # clear Shell
os.system('clear')



banner = pyfiglet.figlet_format("Folcoxx SCANNER")
print(banner)



remoteServer = input("Enter a remote host or IP to scan: ")

PortRange = input("Port range (1,1024): ")





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
    remoteHostname = socket.gethostbyaddr(remoteServerIP)
    print("[+] Scanning", remoteHostname)

dt = datetime.now() #Check Start time

try:
    if PortRange.find(',') != -1:
        PortRange1, PortRange2 = PortRange.split(",")
        for port in range(int(PortRange1) , int(PortRange2)+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print("[+] Port {}:  Open".format(port))
            #if result == 10060:
            #    print("[+] Port {}:  closed".format(port))
            #sock.close()

    else:
        port = int(PortRange)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print("[+] Port {}:  Open".format(port))
        if result == 10060:
            print("[+] Port {}:  closed".format(port))
        sock.close()


except KeyboardInterrupt:
    sys.exit()

except socket.error:
    print("No connect to serveur")
    sys.exit()