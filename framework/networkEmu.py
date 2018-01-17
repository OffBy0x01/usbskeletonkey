#imports
import os
import sys
import subprocess


#USB OTG requirements
gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
gether_up = "ifup usb0"
gether_remove = "modprobe -r g_ether"


def network_on(on):

def network_up(up):

def network_down(down):

def network_remove(remove):










# Network Emulation - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class NetworkObject(object):
    """ Class for the Network Object """

    def __init__(self, state):
        self.state = state

    def network_state(self):
        # retrieves the current state of the network and displays it (debug)
        print NetworkObject.state()

