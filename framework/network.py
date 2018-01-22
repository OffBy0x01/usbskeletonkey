import subprocess

from framework.FwComponentGadget import FwComponentGadget


class FwComponentNetwork(FwComponentGadget):
    """ Class for the Network Object

         Args:
            driver_name:    the driver being used e.g. g_hid
            enabled:         manages the on/off state

        functions:
            enable:         allows for enabling of driver
            disable:        allows for disabling of driver
            network_on:     allows for the ethernet adapter to be turned on
            network_off:    allows for the ethernet adapter to be turned off
            network_remove: allows for disable() to be called to disable and remove the driver

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
        self.ping_address = "8.8.8.8"
        self.ping_response = ""

    def __del__(self):
        self.network_remove()

    # Turning on USB Ethernet adapter
    def network_on(self):
        subprocess.call("%s" % self.ether_up, shell=True)
        self.state = "Ethernet adapter up"
        self.ping_test()

    # Turning off USB Ethernet adapter
    def network_off(self):
        subprocess.call("%s" % self.ether_down, shell=True)
        self.state = "Ethernet adapter down"

    # Removing USB Ethernet
    def network_remove(self):
        super().disable()
        self.state = "uninitialised"

    def ping_test(self):
        self.ping_response = subprocess.call("ping -c 1 " + self.ping_address)
        if self.ping_response == 0:
            super().debug("ping successful!")
            return
        else:
            super().debug("Ping unsuccessful!")









