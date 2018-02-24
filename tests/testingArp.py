import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.arp import ipIsValid, arpScan

print(ipIsValid("127.00.0.001"))

print(ipIsValid("1127.00.000.256"))

print(ipIsValid("127.0.0.0/24"))

print(ipIsValid("127.0.0.0-127.0.0.255"))  # This should be valid usage but its not working with the command

output = arpScan("192.168.0.0/24", interface="wlan0")

print(output)
