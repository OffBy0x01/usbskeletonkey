'''
This file is to load a file system onto the connected host.

This file will have an accompanying file system to clone for each run.

This file system could also be loaded via loop back to save the outputs of modules
'''

import sys

from framework import FwComponent

temp = 'Later'

class StorageAccess(FwComponent):

    def __convertsize(self, readable_size):
        #Function that the class will use to check file sizes
        true_size = temp # This conversion will be the opposite of Dive into pythons. Fun!
        return true_size

    def __init__(self, readable_size, debug=False):
        #Create device to store to
        #sudo dd if=/dev/zero of=Desktop/storageTemplate.bin bs=512 count=size/512
        self.loopback_device = temp #sudo losetup -f # To find the first available loop back
        self._readable_size = readable_size
        self._size = self.__convertSize(readable_size)
        self.self_mounted = False
        self.bus_mounted = False

    def __del__(self):
        # No matter what call umount?
        self.umount()
        # Then unmount from loopback
        # There is not a circumstance where it would be a good idea to allow the user to do this via umount

    def __sizeof__(self): return self._size # machine readable sizeof is default defined

    def sizeof(self): return self._readable_size # human readable sizeof is human defined


    def mountLocal(self, directory, read_only=False):
        #Mount the file system locally for amending
        '''
        #Figure out the commands for this
        >>>if readonly: #mount RO
        >>>else: #mount norm
        >>>return 0
        '''

    def mountBus(self, _write_block):
        #Mount over USB
        '''
        #If writeblock is possible
        >>>if _write_block: #mount RO
        >>>else: #mount norm
        >>>return 0
        '''

    def umount(self):
        """
        Void function that will unmount from whatever the class is currently mounted to
        """
        if not self.self_mounted:
             if not self.bus_mounted:
                 return
             else:
                 #unmount from bus
        else:
            #unmount from self
        return
