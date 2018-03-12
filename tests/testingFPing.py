import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.fping import *

# IPs = ["192.168.0.0/24", "192.168.1.0/24"]
# IP = "127.0.0.1"

# print(ipIsValid("192.168.0.0/24"))

# Currently unable to get good output from host names, Tempted to void this functionality

output = fping("www.google.com", get_ips_from_dns=True)

print(output)

'''
# Tests for parsing the output from multiple pings

# takes in IP : ping stats
# gives out ["IP", "ping stats"]

pings = 4

output = fping("8.8.8.8", ping_count=pings)

if pings > 0:
    output = output.split(" : ")

print(output)
'''
