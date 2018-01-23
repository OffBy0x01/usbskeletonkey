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
            network_kill:   allows for the Ethernet Adapter to be disabled and removed if
                            a ping fails
        Returns:
            framework component object

        Raises:
            ImportError when kernel module not found
    """

    # Constructor
    def __init__(self, enabled=False, debug=True, state="uninitialised"):
        super().__init__(driver_name="g_ether", enabled=enabled, vendor_id="0x04b3", product_id="0x4010", debug=debug)
        self.debug = debug
        self.state = state
        self.ether_up = "ifup usb0"
        self.ether_down = "ifdown usb0"
        self.state = "initialised"
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
            if not self.ping_on:  # If not already pinging
                self.ping_on = True
                self.ping_response = subprocess.call("ping -c 1 -w 3 " + self.ping_address, shell=True)  # Ping to test connection
                self.ping_on = False
                if self.ping_response == 0:  # If ping successful
                    super().debug("Ping successful!")
                    flag_success = True
                    counter = 3  # Exit loop
                else:  # If ping not successful
                    super().debug("Ping unsuccessful!")
                    counter += 1  # Try again
            else:
                super().debug("Ping already in use")
        if not flag_success:  # If 3 ping attempts fail
            self.kill("Connection failed!")  # Kill process
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
        while True:  # Wait till active ping tests are done
            if not self.ping_on:  # If no active ping tests
                super().debug(error_message)  # Debug text
                self.network_remove()  # Detach from bus
                return


test = FwComponentNetwork()
test.network_on()