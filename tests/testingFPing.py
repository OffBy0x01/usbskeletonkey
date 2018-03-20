import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.fping import *

# IPs = ["192.168.0.0/24", "192.168.1.0/24"]
# IP = "127.0.0.1"

# print(is_valid_ipv4_address("192.168.0.0/24"))

# Currently unable to get good output from host names, Tempted to void this functionality
'''
output = check_target_is_alive("www.google.com", get_ips_from_dns=True, get_dns_name=True)

print(output)

'''
# Tests for parsing the output from multiple pings

# takes in IP : ping stats
# gives out ["IP", "ping stats"]

pings = 4

output = check_target_is_alive("8.8.8.0/28", ping_count=pings, interface="wlp4s0b1")

output = output.split("\n")
output.pop()

output_final = []

if type(output) is list:
    for item in output:
        if pings > 0:
            output_final += [item.split(" : ")]
    print(output_final)
else:
    if pings > 0:
        output = output.split(" : ")
    print(output)
