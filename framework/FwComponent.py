import subprocess


class fw_component_dr(object):
    """ This defines the construction of framework components.
        Use with inheritance, do not use on its own.

    Args:
        driver_name:    the driver being used e.g. g_hid
        enable:         manages the on/off state

    functions:
        enable:         allows for enabling of driver
        disable:        allows for disabling of driver

    Returns:
        framework component object

    Raises:
        ImportError when kernel module not found
    """

    def __init__(self, driver_name, enabled=False, vendor_id="", product_id=""):
        """Return a new framework component"""
        self.driver_name = driver_name
        # If kernel module was not found then modprobe -n will return x not found in y - this can be used to detect if our stuff is there
        if "not found" in subprocess.run(["modprobe", "-n", driver_name], stdout=subprocess.PIPE).stdout.decode(
                'utf-8'):
        # THROW EXCEPTION HERE

        self.enabled = enabled
        self.vendor_id = vendor_id
        self.product_id = product_id

    def enable(self):
        """Enable a disabled framework object"""
        if not self.enable:
            subprocess.call("modprobe %s %s %s" % (driver_name, vendor_id, product_id), shell=True)
            self.enabled = True
        else:
            print('Driver already enabled!')

    def disable(self):
        """Disable an enabled framework object"""
        if self.enabled:
            subprocess.call("modprobe -r %s" % driver_name, shell=True)
            self.enabled = False
        else:
            print('Driver already disabled!')
