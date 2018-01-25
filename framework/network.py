import subprocess
import time

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

    def __init__(self, enabled=False, debug=False, state="uninitialised"):
        super().__init__(driver_name="g_ether", enabled=enabled, vendor_id="0x04b3", product_id="0x4010", debug=debug)
        self.debug = debug
        self.state = state
        self.ether_up = "ifup usb0"
        self.ether_down = "ifdown usb0"
        self.state = "initialised"
        self.ping_address = "8.8.8.8"
        self.ping_response = ""
        self.timer_start = time.time()
        self.timer_end = ""

    def __del__(self):
        self.network_remove()

    # Turning on USB Ethernet adapter
    def network_on(self):

        subprocess.call("%s" % self.ether_up, shell=True)
        self.state = "Ethernet adapter up"
        if self.debug:
            super().debug(self.state)
        self.ping_test()
        return

    # Turning off USB Ethernet adapter
    def network_off(self):
        subprocess.call("%s" % self.ether_down, shell=True)
        self.state = "Ethernet adapter down"
        if self.debug:
            super().debug(self.state)
        time.sleep(9)
        self.timer_end = time.time()
        print (self.timer_end - self.timer_start)
        return

    # Removing USB Ethernet
    def network_remove(self):
        super().disable()
        self.state = "uninitialised"
        if self.debug:
            super().debug(self.state)
        return

    # Check for internet connectivity
    def ping_test(self):
        self.ping_response = subprocess.call("ping -c 1 " + self.ping_address)
        if self.ping_response == 0:
            super().debug("ping successful!")

        else:
            super().debug("Ping unsuccessful!")
        return

    #def kill_switch(self):
# if time > 5 mins:
    # do kill switch
    #test



test = FwComponentNetwork()
test.network_off()




