#imports
import os
import sys
import subprocess

# Interface - 17th of January 2018
# by Michaela Stewart and Jonathan Ross

class InterfaceObject(object):
    """ Class for the Interface Object """

    title = "'Skeleton Key Project'"

    def __init__(self, modules, exit_flag):
        self.modules = modules
        self.exit_flag = exit_flag

    def display_title(self):
        print InterfaceObject.title()

    def display_modules(self):
        if range(len(self.modules)) == 0:
            print "There are no modules to display."
        else:
            for module in range(len(self.modules)):
                print (module+1), " ", self.modules[module]

# Main Program
# Load in Module file
test_file = [ "Responder", "NMap", "Enumeration"]
intro = InterfaceObject(test_file, 0)

# Display title
intro.display_title()
# Display modules
intro.display_modules()

