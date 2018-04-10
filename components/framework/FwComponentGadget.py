import subprocess

from components.framework.Debug import Debug
from components.helpers.Format import Format


class FwComponentGadget():
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

    def __init__(self, driver_name, enabled=False, vendor_id="", product_id="", debug=False, name="debug",
                 type="component"):
        """Return a new framework component"""
        self.gadget = Debug(name=name, type=type, debug=debug)
        self.driver_name = driver_name
        # If kernel module was not found then modprobe -n will return driver_name not found in modules
        if "not found" in subprocess.run(["modprobe", "-n", driver_name], stdout=subprocess.PIPE).stdout.decode(
                'utf-8'):  # THROW EXCEPTION HERE
            self.gadget.debug("CRITICAL: %s does not exist" % driver_name, color=Format.color_danger)
        self.driver_name = driver_name

        if enabled:
            self.enable()

        self.enabled = enabled;

        self.vendor_id = vendor_id
        self.product_id = product_id

    def enable(self):
        """Enable a disabled framework object"""
        if not self.enabled:
            subprocess.call("modprobe %s %s %s" % (self.driver_name, self.vendor_id, self.product_id), shell=True)
            self.gadget.debug(self.enabled)
            self.enabled = True
        else:
            self.gadget.debug("Driver already enabled: %s" % self.enabled, color=Format.color_info)

    def disable(self):
        """Disable an enabled framework object"""
        try: # This might be called on destroy, which can throw an error.
            if self.enabled:
                subprocess.call("modprobe -r %s" % self.driver_name, shell=True)
                self.enabled = False
            else:
                self.gadget.debug("Driver already disabled: %s" % True, color=Format.color_info)
        except Exception:
            self.gadget.debug("Driver already disabled: %s" % True, color=Format.color_info)

    def status(self):
        """Return the driver status"""
        self.gadget.debug("Driver enabled: %s" % self.enabled, color=Format.color_info)
        return self.enabled
