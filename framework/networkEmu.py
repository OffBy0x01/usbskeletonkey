#imports
import os
import sys
import subprocess

# Network Emulation - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class NetworkObject(object):
    """ Class for the Network Object """

    # USB OTG requirements
    gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
    gether_up = "ifup usb0"
    gether_remove = "modprobe -r g_ether"

    def __init__(self, state):
        self.state = state

    def network_state(self):
        # retrieves the current state of the network and displays it (debug)
        print NetworkObject.state()

    def network_on(self):
        # pass gether to bash
        pass

    def network_initialise(self):
        pass

    def network_down(self):
        pass

    def network_remove(self):
        pass



