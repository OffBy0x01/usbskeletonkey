import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.modules.NMAP import *

# Testing
test = NMAP()
test.os_detection()