import os
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.Enumerate.Enumerate import Enumerate

IPs = "127.0.0.0"
# IP = "127.0.0.1"

output = Enumerate.check_target_is_alive(IPs,
                                         interface="wlp4s0b1",
                                         ping_count=4,
                                         verbose=True)

print(output)
