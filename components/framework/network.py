import subprocess

from components.framework.FwComponentGadget import FwComponentGadget
from components.framework.Debug import Debug


class FwComponentNetwork(FwComponentGadget):
    """ Class for the Network Object

         Args:
            state:          state of driver
            enabled:        manages the on/off state
            debug:          for enabling debug text

        functions:
            disable:        allows for the disabling of driver
            up:             allows for the driver to be turned on and DHCP to be enabled
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
        self.state = state
        self.ping_address = "8.8.8.8"
        self._type = "Component"
        self._name = "Network"

        self.network = Debug(name="Network", type="Framework", debug=debug)

    # Destructor
    def __del__(self):
        if self.state == "usb0 down":
            super().disable()  # Disable eth driver
        else:
            self.down()  # Ensure adapter is downed
            super().disable()  # Disable eth driver

    # Check for internet connectivity
    def test_internet(self):
        flag_success = False  # Flag set when connection successful
        for i in range(1, 3):  # Only attempt ping 3 times
            if subprocess.call("ping -c 1 -w 3 " + self.ping_address, shell=True) == 0:  # Ping to test connection
                self.network.debug("Ping successful!")
                # Exit loop
                flag_success = True
                break
            else:  # If ping not successful
                self.network.debug("Ping unsuccessful!")
                # Try again
        if not flag_success:  # If 3 ping attempts fail
            return self.kill("Connection failed!")
        return True

    # Find instance of "USB" in ifconfig to show that usb0 is connected
    def test_local(self):
        output = str(subprocess.run(["ifconfig"], stdout=subprocess.PIPE).stdout.decode())
        self.debug(output)
        if (output.count("usb0")) > 0:
            self.network.debug("usb0 detected")
            return True
        else:
            return self.kill("usb0 not detected")

    # Turning on USB Ethernet adapter and enabling DHCP server
    def up(self):
        self.enable()

        self.network.debug("Failed to ifup usb0" if subprocess.call("ifup usb0", shell=True) else "usb0 ifup successful")  # Up usb0 interface
        self.network.debug("Failed to up networking on usb0" if subprocess.call("ifconfig usb0 up", shell=True) else "usb0 networking up")  # Up networking on usb0
        self.network.debug("Failed to add IP routes to usb0" if subprocess.call("/sbin/route add -net 0.0.0.0/0 usb0", shell=True) else "usb0 IP routes added successfully")  # Add route for all IPv4 addresses
        self.network.debug("Failed to start DHCP server" if subprocess.call("/etc/init.d/isc-dhcp-server start", shell=True) else "DHCP server successfully started")  # Start DHCP server
        self.network.debug("Failed to enable IPv4 forwarding" if subprocess.call("/sbin/sysctl -w net.ipv4.ip_forward=1", shell=True) else "IPv4 forwarding successfully enabled")  # Enable IPv4 forwarding
        self.network.debug("Failed to bind port 80 to 1337" if subprocess.call("/sbin/iptables -t nat -A PREROUTING -i usb0 -p tcp --dport 80 -j REDIRECT --to-port 1337", shell=True) else "Successfully binded port 80 to port 1337")  # Bind port 80 to port 1337
        self.network.debug("Failed to start dnsspoof on port 53" if subprocess.call("/usr/bin/screen -dmS dnsspoof /usr/sbin/dnsspoof -i usb0 port 53", shell=True) else "Successfully started dnsspoof on port 53")  # Start dnsspoof on port 53
        self.state = "usb0 should be up"
        if self.network.debug:  # Debug text
            self.network.debug(self.state)
        return self.test_local()  # Test connection

    # Turning off USB Ethernet adapter
    def down(self):
        self.network.debug("Failed to disable IPv4 forwarding" if subprocess.call("/sbin/sysctl -w net.ipv4.ip_forward=0", shell=True) else "IPv4 forwarding successfully disabled")  # Disable IPv4 forwarding
        self.network.debug("Failed to stop DHCP server" if subprocess.call("/etc/init.d/isc-dhcp-server stop", shell=True) else "DHCP server successfully stopped")  # Stop DHCP server
        self.network.debug("Failed to remove IP routes from usb0" if subprocess.call("/sbin/route del -net 0.0.0.0/0 usb0", shell=True) else "usb0 IP routes removed successfully")  # Remove route for all IPv4 addresses

        # Down adapter
        self.network.debug("Failed to down networking on usb0" if subprocess.call("ifconfig usb0 down", shell=True) else "usb0 networking down")
        self.network.debug("Failed to ifdown usb0" if subprocess.call("ifdown usb0", shell=True) else "usb0 ifdown successful")

        # Debug
        self.state = "usb0 down"
        self.network.debug(self.state)

    # Removing USB Ethernet
    def disable(self):
        super().disable()  # Call parent class to remove the driver
        self.state = "uninitialised"
        self.network.debug(self.state)
        return

    # Emergency Kill
    def kill(self, error_message):
        super().debug(error_message)  # Debug text
        self.disable()  # Detach from bus
        return
