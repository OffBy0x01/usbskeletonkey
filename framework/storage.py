import subprocess

from datetime import datetime
from framework import FwComponentGadget


class StorageAccess(FwComponentGadget):
    """This allows for creation of mini file systems that can be used for storing locally or via the bus
    If this is closed early it will fuck up pretty bad and will require a restart of the device

    Args:
        readable_size:  Input the size of the file system intended e.g 1M or 512K

        debug:          Boolean value for the state of Debug prints

    functions:
        alot:           Ill get back to this

    Returns:
        tbd

    Raises:
        tbd
    """

    def __init__(self, readable_size, filesystem="FAT", debug=False):
        # There might be an alternative I'll look into
        self.readable_size = readable_size

        # Create device to store to
        self.file_name = datetime.now().strftime('%Y-%m-%d--%H:%M.img')

        # Makes a file system.
        # These don't have output of note (I should look for the error messages and check the Pi is ok with this)
        subprocess.run(["fallocate", "-l", self.readable_size, self.file_name])

        # Format file system to FAT ... for now
        subprocess.run(["mkfs.fat", self.file_name])
        # compgen -c | grep "mkfs\." # Lists all file systems


        # To find the first available loop back
        self.loopback_device = subprocess.run(["losetup", "-f"],stdout=subprocess.PIPE).stdout.decode('utf-8')
        if debug: print("Temp")  # Debug out what device is intended of use

        self.local_mounted = False
        self.bus_mounted = False
        return

    def __del__(self):
        # No matter what call unmount?
        self.umount()
        # Then unmount from loopback
        # There is not a circumstance where it would be a good idea to allow the user to do this via umount
        return

    def __sizeof__(self):  return self.readable_size  # machine readable sizeof is default defined

    def mountlocal(self, directory, read_only=False):
        # Mount the file system locally for amending
        # The commands are needed for this
        if read_only: # mount RO
        else: #mount norm
            return
    '''
    def mountbus(self, _write_block):
        # Mount over USB
        #If write block is possible
        if _write_block:  # mount RO
        else:  # mount norm
            return

    def unmountbus(self):
        self.bus_mounted = False
        return
    '''
    def unmountlocal(self):
        self.local_mounted = False
        return
    '''
    def unmount(self):
        """
        Void function that will unmount from whatever the class is currently mounted to
        """
        if not self.local_mounted:
            if not self.bus_mounted:
                return
            else:
                self.umountbus()
        else:
            self.umountlocal()
        return
    '''
