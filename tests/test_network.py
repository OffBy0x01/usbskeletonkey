import os.path
import sys
import time

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components.framework.network import FwComponentNetwork

# For testing
if __name__ == "__main__":
    test = FwComponentNetwork(debug=True)
    test.up()
    time.sleep(30)  # sleep for 30 secs for testing purposes


