'''
This file is to load a file system onto the connected host.

This file will have an accompanying file system to clone for each run.

This file system could also be loaded via loopback to save the outputs of modules
'''

import FwComponent

class storageAccess(fw_component_dr)

    def __init__(self, other):
        #Copy the template to make a little memory file for this run

    def mountLocal(self, directory):
        #Mount the file system locally for ammending

    def mountBus(self):
        #Mount over USB
