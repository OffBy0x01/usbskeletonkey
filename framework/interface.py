""" Interface v1.0 (first draft) for 'Skeleton Key' """
# imports

from framework import FwComponent


class ModuleObjects(FwComponent):
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
    """
     Class for the Interface Object

         Args:
            module:             list of the modules
            title:              title of the application "Skeleton Key"

        functions:
            display_title:      displays the title of the application on screen.
            display_modules:    displays all the modules on screen - loaded from the list of modules

        Returns:
            the UI

        Raises:
            No modules found in list - empty list
            Invalid user input - string
            Invalid user input - index of module not listed (e.g. <0 or >list)
    """

    def __init__(self, modules={2, 3, 4}):  # If you remove this default it may fix the problem in display modules if
                                            # the problem persists
        self.modules = modules
        self.title = "'Skeleton Key Project'"

    def display_title(self):
        print(self.title)

    def display_modules(self):
        if not self.modules:
            print("There are no modules to display.")
        else:
            for module in self.modules:
                print(module + 1, " ", self.modules[module])

    def bool_ask_question(self, question):
        """ Desc:
                Enables asking of y/n questions"""

    def input_choice(self):
        exit_flag = False
        while not exit_flag:
            # Display title
            intro.display_title()  # Should this not be self. Since intro is the debug name but not necesarily the name
            # Display modules
            intro.display_modules()  # Should this not be self

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
                    exit(0)


# debugging
if __name__ == '__main__':
    test_file = ["Responder", "NMap", "Enumeration"]
    intro = InterfaceObject(test_file)
