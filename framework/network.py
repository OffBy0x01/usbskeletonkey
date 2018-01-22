import subprocess
import time

from framework import FwComponentGadget


# -*- coding: utf-8 -*-


class fw_component_network(FwComponentGadget):
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
    def __init__(self, debug=False, state="uninitialised"):
        super().__init__(driver_name="g_ether", enabled=False, vendor_id ="0x04b3", product_id ="0x4010", debug=False)
        self.debug = debug
        self.state = state
        self.ether_up = "ifup usb0"
        self.ether_down = "ifdown usb0"
        super().enable()  # Initialising Ethernet
        self.state = "initialised"

    # Turning on USB Ethernet adapter
    def network_on(self):
        subprocess.call("%s" % self.ether_up, shell=True)
        self.state = "Ethernet adapter up"

    # Turning off USB Ethernet adapter
    def network_down(self):
        subprocess.call("%s" % self.ether_down, shell=True)
        self.state = "Ethernet adapter down"

    # Deconstructor
    def __del__(self):
        self.network_remove()

    # Removing USB Ethernet
    def network_remove(self):
        super().disable()
        self.state = "uninitialised"



