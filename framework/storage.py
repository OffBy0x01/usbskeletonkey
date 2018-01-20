import subprocess

from framework import FwComponentGadget

temp = 'Later'


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

    def __convertsize(self, readable_size):
        # Function that the class will use to check file sizes
        true_size = readable_size  # This conversion will be the opposite of Dive into pythons. Fun!
        return true_size

    def __init__(self, readable_size, debug=False):
        super().__init__(driver_name="", enabled=False, debug=False)
        # Translate the provided size
        self._size = self.__convertSize(readable_size)

        # Create device to store to
        self.__readable_size = readable_size
        # dd if=/dev/zero of=Desktop/storageTemplate.bin bs=512 count=size/512

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

    def __sizeof__(self): return self._size  # machine readable sizeof is default defined

    def sizeof(self): return self._readable_size  # human readable sizeof is human defined

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
