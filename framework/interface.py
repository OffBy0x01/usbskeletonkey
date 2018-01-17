# imports
import os
import sys
import subprocess


# Interface - 17th of January 2018
# by Michaela Stewart and Jonathan Ross


class ModuleObjects(object):
    """ Class for Module Objects"""

    def __init__(self, index, name, nes_modules):
        self.index = index
        self.name = name
        self.nes_modules = nes_modules


module_1 = ModuleObjects(1, "Responder", 1)
module_2 = ModuleObjects(2, "NMap", 12)
module_3 = ModuleObjects(3, "Enumeration", 23)


class InterfaceObject(object):
    """ Class for the Interface Object """

    title = "'Skeleton Key Project'"

    def __init__(self, modules, exit_flag):
        self.modules = modules
        self.exit_flag = exit_flag

    def display_title(self):
        print InterfaceObject.title

    def display_modules(self):
        if range(len(self.modules)) == 0:
            print "There are no modules to display."
        else:
            for module in range(len(self.modules)):
                print (module + 1), " ", self.modules[module]


# Main Program
# Load in Module file
test_file = ["Responder", "NMap", "Enumeration"]
intro = InterfaceObject(test_file, False)

# Display title
intro.display_title()
# Display modules
intro.display_modules()

if intro.exit_flag == True:
    # Run end program
    pass
else:
    valid = False
    while valid != True:
        user_selection = int(raw_input("Please enter the module you would like to configure. (Based on index)"))
        if user_selection == str:
            print "Error 101: Invalid selection - string instead of integer."
            pass
        elif user_selection <= 0 or user_selection > len(intro.modules):
            print "Error 102: Invalid index selection. Please enter a valid selection."
            pass
        else:
            valid = True
            pass
