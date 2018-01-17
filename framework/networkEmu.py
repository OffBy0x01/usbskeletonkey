import os
import sys
import subprocess
import time
import FwComponent

# Network Emulation - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class fw_component_network(FwComponent):
    """ Class for the Network Object """

    # USB OTG requirements
    gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
    gether_up = "ifup usb0"
    gether_down = "ifdown usb0"
    gether_remove = "modprobe -r g_ether"

    def __init__(self, debug=False, state=""):

    def network_on(self):
        subprocess.call("%s" % fw_component_network.gether, shell=True)
        time.sleep(1)
        subprocess.call("%s" % fw_component_network.gether_up, shell=True)
        fw_component_network.state = "initialised"

    def network_down(self):
        subprocess.call("%s" % fw_component_network.gether_down, shell=True)
        fw_component_network.state = "down"


    def network_remove(self):
        self.state = "State: Network Emulation Has been removed or not initilaised"
        fw_component_network.state = "uninitialised"





run=fw_component_network()

state=run.network_remove()

print()


