import os
import sys

# Network Emulation - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class NetworkObject(object):
    """ Class for the Network Object """

    def __init__(self, state):
        self.state = state

    def network_state(self):
        # retrieves the current state of the network and displays it (debug)
        print NetworkObject.state()

