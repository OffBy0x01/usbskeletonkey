'''
This file is to load a file system onto the connected host.

This file will have an accompanying file system to clone for each run.

This file system could also be loaded via loop back to save the outputs of modules
'''

import sys


from framework import FwComponent

class storageAccess(FwComponent)

    def __init__(self, __readable_size):
        #Create device to store to
        #sudo dd if=/dev/zero of=Desktop/storageTemplate.bin bs=512 count=size/512
        self._size = approximate_size(__readable_size)

    def __del__(self):
        # No matter what call umount?
        self.umount()

    def __sizeof__(self):
        return self._size

    def mountLocal(self, directory):
        #Mount the file system locally for amending

    def mountBus(self):
        #Mount over USB

    def umount(self):
        #unmount all -- this should be called on class destruction

    def _convertSize(self):
        #Function that the class will use to check file sizes
