import os
import sys
import subprocess
import time
from framework import FwComponent

# -*- coding: utf-8 -*-


class fw_component_network(FwComponent):
    """ Class for the Network Object

         Args:
            driver_name:    the driver being used e.g. g_hid
            enabled:         manages the on/off state

        functions:
            enable:         allows for enabling of driver
            disable:        allows for disabling of driver

        Returns:
            framework component object

        Raises:
            ImportError when kernel module not found
        """

    # USB OTG requirements
    gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
    gether_up = "ifup usb0"
    gether_down = "ifdown usb0"
    gether_remove = "modprobe -r g_ether"

    def __init__(self, debug=False, state=""):
        self.debug = debug
        self.state = state

    # Initialising and turning on USB Ethernet
    def network_on(self):
        subprocess.call("%s" % fw_component_network.gether, shell=True)
        time.sleep(1)
        subprocess.call("%s" % fw_component_network.gether_up, shell=True)
        fw_component_network.state = "initialised"

    # Turning off USB Ethernet
    def network_down(self):
        subprocess.call("%s" % fw_component_network.gether_down, shell=True)
        fw_component_network.state = "down"

    # Removing USB Ethernet OTG module
    def network_remove(self):

        fw_component_network.state = "uninitialised"





# run=fw_component_network()

# state=run.network_remove()
# print()


