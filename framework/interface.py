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
        print InterfaceObject.title

    def display_modules(self):
        if range(len(self.modules)) == 0:
            print "There are no modules to display."
        else:
            for module in range(len(self.modules)):
                print (module+1), " ", self.modules[module]


# Main Program
# Load in Module file
test_file = {
    1, "Responder", [1],
    2, "NMap", [1, 2],
    3, "Enumeration", [2, 3]
}
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
        if type(user_selection) != int or user_selection >= 0 or user_selection < len(intro.modules):
            print "Error 101: Invalid index selection. Please enter a valid selection."
            pass
        else:
            valid = True
