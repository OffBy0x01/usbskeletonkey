import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.arp import is_valid_ipv4_address, get_targets_via_arp

IPs = ["192.168.1.0"]
# IPs = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
# IP = "127.0.0.1"

#print(is_valid_ipv4_address(<test>)

output = get_targets_via_arp(IPs, interface="wlp4s0b1")

print(output)
