'''
This file is to load a file system onto the connected host.

This file will have an accompanying file system to clone for each run.

This file system could also be loaded via loop back to save the outputs of modules
'''

from framework import FwComponent

class storageAccess(fw_component_dr)

    def __init__(self, size, other):
        #Create device to store to
        self.size = approximate_size(size)

    def mountLocal(self, directory):
        #Mount the file system locally for amending

    def mountBus(self):
        #Mount over USB
