import os
import sys
import subprocess
import time
from framework import FwComponent

# -*- coding: utf-8 -*-

class fw_component_network(FwComponent):

    """ Class for the Network Object

         Args:
            state:          Determines what "state" g_ether is in i.e. initialised or disabled
            debug:          Bool value to enable or disable debug mode

        functions:
            network_on:     allows for Ethernet driver to be added and initialised
            network_down:   allows for Ethernet driver to be turned off
            network_remove:  allows for Ethernet driver to be removed

        Returns:
            To Do

        Raises:
            To Do
        """

    # USB OTG requirements
    gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
    gether_up = "ifup usb0"
    gether_down = "ifdown usb0"
    gether_remove = "modprobe -r g_ether"


    def __init__(self, debug=False, state=""):

    #Initialising and turning on USB Ethernet
    def network_on(self):
        subprocess.call("%s" % fw_component_network.gether, shell=True)
        time.sleep(1)
        subprocess.call("%s" % fw_component_network.gether_up, shell=True)
        fw_component_network.state = "initialised"

    # Turning off USB Ethernet
    def network_down(self):
        subprocess.call("%s" % fw_component_network.gether_down, shell=True)
        fw_component_network.state = "down"

    # Removing USB Ethernet
    def network_remove(self):
        subprocess.call("%s" % fw_component_network.gether_remove, shell=True)
        fw_component_network.state = "uninitialised"



#run=fw_component_network()

#state=run.network_remove()
#print()


