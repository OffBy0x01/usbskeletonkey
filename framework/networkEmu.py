import os
import sys
import subprocess
import time

# Network Emulation - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class fw_component_network(object):
    """ Class for the Network Object """

    # USB OTG requirements
    gether = "modprobe g_ether idVendor=0x04b3 idProduct=0x4010"
    gether_up = "ifup usb0"
    gether_down = "ifdown usb0"
    gether_remove = "modprobe -r g_ether"


    def network_on(self):
        subprocess.call("%s" % fw_component_network.gether, shell=True)
        time.sleep(1)
        subprocess.call("%s" % fw_component_network.gether_up, shell=True)
        self.state = "State: Network Emulation on"
        return self.state


    def network_down(self):
        subprocess.call("%s" % fw_component_network.gether_down, shell=True)
        self.state = "State: Network Emulation Down"
        return self.state


    def network_remove(self):
        self.state = "State: Network Emulation Has been removed or not initilaised"
        return self.state


run=fw_component_network()

state=run.network_down()

print(state)

