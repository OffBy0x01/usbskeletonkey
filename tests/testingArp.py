import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.arp import ipIsValid, arpScan

IPs = ["192.168.0.0/24", "192.168.1.0/24"]
# IP = "127.0.0.1"

#print(ipIsValid(<test>)

output = arpScan(IPs, interface="wlp4s0b1")

print(output)
