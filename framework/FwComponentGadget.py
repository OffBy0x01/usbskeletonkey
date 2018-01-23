import subprocess

from framework.FwComponent import FwComponent


class FwComponentGadget(FwComponent):
    """Parent class for components requiring use of usb_gadget

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

    def __init__(self, driver_name, enabled=False, vendor_id="", product_id="", debug=False):  # enabled=True or enabled=enabled?
        """Return a new framework component"""

        self.driver_name = driver_name
        # If kernel module was not found then modprobe -n will return x not found in y
        if "not found" in subprocess.run(["modprobe", "-n", driver_name], stdout=subprocess.PIPE).stdout.decode(
                'utf-8'):  # THROW EXCEPTION HERE
            print("THROW EXCEPTION HERE")

        self.driver_name = driver_name
        self.enabled = enabled
        self.vendor_id = vendor_id
        self.product_id = product_id

        # set debug state
        super().__init__(debug=debug)

    def enable(self):
        """Enable a disabled framework object"""
        if not self.enable:
            subprocess.call("modprobe %s %s %s" % (self.driver_name, self.vendor_id, self.product_id), shell=True)
            self.enabled = True
        else:
            super().debug('Driver already enabled!')

    def disable(self):
        """Disable an enabled framework object"""
        if self.enabled:
            subprocess.call("modprobe -r %s" % self.driver_name, shell=True)
            self.enabled = False
        else:
            super().debug('Driver already disabled!')

    def status(self):
        """Return the driver status"""
        if self.enabled:
            super().debug("Driver enabled")
        else:
            super().debug("Driver disabled")
        return self.enabled
