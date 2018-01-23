import subprocess

from framework.FwComponentGadget import FwComponentGadget


class FwComponentNetwork(FwComponentGadget):
    """ Class for the Network Object

         Args:
            state:          state of driver
            enabled:        manages the on/off state
            debug:          for enabling debug text

        functions:
            enable:         allows for enabling of driver
            disable:        allows for disabling of driver
            network_on:     allows for the ethernet adapter to be turned on
            network_off:    allows for the ethernet adapter to be turned off
            network_remove: allows for disable() to be called to disable and remove the driver
            network_kill:   allows for the Ethernet Adapter to be disabled and removed if
                            a ping fails

        Returns:
            framework component object

        Raises:
            Critical error if connection is not established
            Error thrown if ping is already in progress
    """

    # Constructor
    def __init__(self, enabled=False, debug=True, state="uninitialised"):
        super().__init__(driver_name="g_ether", enabled=enabled, vendor_id="0x04b3", product_id="0x4010", debug=debug)
        self.debug = debug
        self.state = state
        self.ether_up = "ifup usb0"
        self.ether_down = "ifdown usb0"
        self.ping_address = "8.8.8.8"
        self.ping_on = False
        self.ping_response = ""

    # Destructor
    def __del__(self):
        self.network_remove()  # Disable eth driver

    # Check for internet connectivity
    def ping_test(self):
        counter = 0
        flag_success = False  # Flag set when connection successful
        while counter < 3:  # Only attempt ping 3 times

            if subprocess.call("ping -c 1 -w 3 " + self.ping_address, shell=True) == 0:  # Ping to test connection
                super().debug("Ping successful!")
                counter = 3  # Exit loop
                flag_success = True
            else:  # If ping not successful
                super().debug("Ping unsuccessful!")
                counter += 1  # Try again
        if not flag_success:  # If 3 ping attempts fail
            super().debug("Connection failed!")
        return

    # Turning on USB Ethernet adapter
    def network_on(self):
        subprocess.call("%s" % self.ether_up, shell=True)  # Up adapter
        self.state = "Ethernet adapter up"
        if self.debug:  # Debug text
            super().debug(self.state)
        self.ping_test()  # Test connection
        return

    # Turning off USB Ethernet adapter
    def network_off(self):
        subprocess.call("%s" % self.ether_down, shell=True)  # Down adapter
        self.state = "Ethernet adapter down"
        if self.debug:  # Debug text
            super().debug(self.state)
        return

    # Removing USB Ethernet
    def network_remove(self):
        super().disable()  # Call parent class to remove the driver
        self.state = "uninitialised"
        if self.debug:  # Debug text
            super().debug(self.state)
        return

    # Emergency Kill
    def kill(self, error_message):
        super().debug(error_message)  # Debug text
        self.network_remove()  # Detach from bus
        return

# For testing
test = FwComponentNetwork()
test.network_on()
