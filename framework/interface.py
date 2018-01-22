""" Interface v1.0 (first draft) for 'Skeleton Key' """
# imports

from framework.FwComponent import FwComponent


class ModuleObjects:
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


class InterfaceObject(FwComponent):
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

    def __init__(self, module_list, debug=False):
        # super().__init__()
        super().debug = debug
        self.module_list = module_list
        self.title = "'Skeleton Key Project'"

    def display_title(self):
        print(self.title)

    def display_modules(self):
        if not self.module_list:
            print("There are no modules to display.")
        else:
            x = 1
            for module in self.module_list:
                print (x, " ", module)
                x += 1

    def bool_ask_question(self, question):
        """ Desc:
                Enables asking of y/n questions"""

    def input_choice(self):
        exit_flag = False
        while not exit_flag:
            # Display title
            self.display_title()  # Should this not be self. Since intro is the debug name but not necesarily the name
            # Display modules
            self.display_modules()  # Should this not be self

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
            elif user_selection < 0 or user_selection > len(self.module_list):
                print("Invalid index selection. Please enter a valid selection.")
                pass
            else:
                if not exit_flag:
                    current_module = test_file[(user_selection - 1)]
                    # mainly for debug
                    # RETURN current_module (move to current_module file)
                    print("Running ", current_module, "...")
                    pass
                else:
                    print("Thank you for using 'Skeleton Key'.")
                    exit(0)


# debugging
if __name__ == '__main__':
    test_file = ["Responder", "NMap", "Enumeration"]
    intro = InterfaceObject(module_list=test_file)
    print(InterfaceObject.display_title(intro))
    print(InterfaceObject.display_modules(intro))
    InterfaceObject.input_choice(intro)
