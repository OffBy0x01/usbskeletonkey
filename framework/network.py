import subprocess

from framework.FwComponentGadget import FwComponentGadget


class FwComponentNetwork(FwComponentGadget):
    """ Class for the Network Object

         Args:
            state:          state of driver
            enabled:        manages the on/off state
            debug:          for enabling debug text

        functions:
            disable:        allows for the disabling of driver
            up:             allows for the driver to be turned on
            down:           allows for the driver to be turned off
            kill:           allows for the driver to be disabled and removed if
                            a ping fails or usb0 isn't recognised
            test_internet:  allows for internet connectivity to be tested
            test_local      checks whether usb0 is recognised by the pi

        Returns:
            framework component object

        Raises:
            import subprocess
    """

    # Constructor
    def __init__(self, enabled=False, debug=True, state="uninitialised"):
        super().__init__(driver_name="g_ether", enabled=enabled, vendor_id="0x04b3", product_id="0x4010", debug=debug)
        self.debug = debug
        self.state = state
        self.ping_address = "8.8.8.8"

    # Destructor
    def __del__(self):
        self.disable()  # Disable eth driver

    # Check for internet connectivity
    def test_internet(self):
        flag_success = False  # Flag set when connection successful
        for i in range(1, 3):  # Only attempt ping 3 times
            if subprocess.call("ping -c 1 -w 3 " + self.ping_address, shell=True) == 0:  # Ping to test connection
                super().debug("Ping successful!")
                # Exit loop
                flag_success = True
                break
            else:  # If ping not successful
                super().debug("Ping unsuccessful!")
                # Try again
        if not flag_success:  # If 3 ping attempts fail
            return self.kill("Connection failed!")
        return True

    # Find instance of "USB" in ifconfig to show that usb0 is connected
    def test_local(self):
        output = str(subprocess.run(["ifconfig"], stdout=subprocess.PIPE).stdout.decode())
        if (output.count("usb0")) > 0:
            super().debug("usb0 detected")
            return True
        else:
            return self.kill("usb0 not detected")

    # Turning on USB Ethernet adapter
    def up(self):
        #  subprocess.call(["./shell_scripts/usb_net_up.sh"])  # Run shell script to enable DHCP server and spoof ports
        subprocess.call("ifup usb0", shell=True)  # Up usb0 interface
        subprocess.call("ifconfig usb0 up", shell=True)  # Up networking on usb0
        subprocess.call("/bin/route add -net 0.0.0.0/0 usb0", shell=True)  # Add route for all IPv4 addresses
        subprocess.call("/etc/init.d/isc-dhcp-server", shell=True)  # Start DHCP server

        # Does things (stolen from poisontap)
        subprocess.call("/sbin/sysctl -w net.ipv4.ip_forward=1", shell=True)  # No idea what this does
        subprocess.call("/sbin/iptables -t nat -A PREROUTING -i usb0 -p tcp --dport 80 -j REDIRECT --to-port 1337", shell=True)  # Bind port 80 to port 1337
        subprocess.call("/usr/bin/screen -dmS dnsspoof /usr/sbin/dnsspoof -i usb0 port 53", shell=True)  # Start dnsspoof on port 53
        self.state = "usb0 up"
        if self.debug:  # Debug text
            super().debug(self.state)
        return self.test_internet()  # Test connection

    # Turning off USB Ethernet adapter
    def down(self):
        #  subprocess.call(["./shell_scripts/usb_net_down.sh"])  # Down adapter
        subprocess.call("/etc/init.d/isc-dhcp-server stop", shell=True)
        subprocess.call("ifconfig usb0 down", shell=True)
        subprocess.call("ifdown usb0", shell=True)
        self.state = "usb0 down"
        if self.debug:  # Debug text
            super().debug(self.state)
        return

    # Removing USB Ethernet
    def disable(self):
        super().disable()  # Call parent class to remove the driver
        self.state = "uninitialised"
        super().debug(self.state)
        return

    # Emergency Kill
    def kill(self, error_message):
        super().debug(error_message)  # Debug text
        self.disable()  # Detach from bus
        return

# TODO #1 network over USB handler
# TODO #2 offline connection status check (must be able to test for physical connection not just internet)
# TODO #3 Read through PiKey, poisontap Source, do some general g_ether research - see what others are using it for


# For testing
if __name__ == "__main__":
    test = FwComponentNetwork()
    test.test_local()
