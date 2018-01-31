import os.path
import sys

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components.framework.network import FwComponentNetwork

# For testing
if __name__ == "__main__":
    test = FwComponentNetwork()
    test.test_local()
