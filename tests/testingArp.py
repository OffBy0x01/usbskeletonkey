import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.Enumerate.Enumerate import Enumerate


IPs = ["192.168.1.1"]
# IPs = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
# IP = "127.0.0.1"

#print(is_valid_ipv4_address(<test>)

output = Enumerate.get_targets_via_arp(IPs, interface="wlp4s0b1")

print(output)
