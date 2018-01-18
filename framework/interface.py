""" Interface v1.0 (first draft) for 'Skeleton Key' """
# imports
import sys


class ModuleObjects(object):
    """
     Class for the Module Object

         Args:
            name:           name of the modules
            nes_modules:    list of module indexes needed to run the current module

        functions:
            none:           currently

        Returns:
            module list

        Raises:
            none currently.
    """

    def __init__(self, name, nes_modules):
        self.name = name
        self.nes_modules = nes_modules


class InterfaceObject(object):
    """ Class for the Interface Object """

    title = "'Skeleton Key Project'"

    def __init__(self, modules):
        self.modules = modules

    def display_title(self):
        print(InterfaceObject.title)

    def display_modules(self):
        if not self.modules:
            print("There are no modules to display.")
        else:
            for module in range(len(self.modules)):
                print(module + 1, " ", self.modules[module])


# Main Program
# Load in Module file
test_file = ["Responder", "NMap", "Enumeration"]
intro = InterfaceObject(test_file)
exit_flag = False

while not exit_flag:
    # clear the screen - os.system('clear')
    # Display title
    intro.display_title()
    # Display modules
    intro.display_modules()

    print("\n")
    print("Enter 0 to exit")
    user_selection = int(input("Please enter the module you would like to configure. (Based on index)"))
    if user_selection == 0:
        print("Exiting Program...")
        exit_flag = True
        pass
    if user_selection == str:
        print("Invalid selection - string instead of integer.")
        pass
    elif user_selection < 0 or user_selection > len(intro.modules):
        print("Invalid index selection. Please enter a valid selection.")
        pass
    else:
        if not exit_flag:
            current_module = test_file[(user_selection - 1)]
            # mainly for debug
            print("Running ", current_module, "...")
            pass
        else:
            print("Thank you for using 'Skeleton Key'.")
            sys.exit(0)