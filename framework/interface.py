""" Interface v1.0 (first draft) for 'Skeleton Key' """
# imports
try:
    import configparser
except ImportError:
    configparser = None
import os
from framework.FwComponent import FwComponent
from framework.helper.ModuleManager import ModuleManager


class ModuleObjects:
    """
     Class for the Module Object

         Args:
            module_name:           name of module
            module_desc:           description of module function
            fw_reqs:               list of framework module requirements
            options:               module specific arguments needed to run
            module_help:           module specific help output
            output_format:         list of definable output formats e.g. XML, plaintext

        functions:
            none:           currently

        Returns:
            module list

        Raises:
            none currently.
    """

    def __init__(self, module_name, module_desc, fw_reqs, options,module_help, output_format):
        self.module_name = module_name
        self.module_desc = module_desc
        self.fw_reqs = fw_reqs
        self.options = options
        self.module_help = module_help
        self.output_format = output_format

    def __exit__(self):
        print("Killing Module object...")
        # if component module object is unresponsive this method provides a kill switch
        for file in self.files:
            os.unlink(file)


class InterfaceObject(FwComponent, ModuleManager):
    """
     Class for the Interface Object

         Args:
            module_list:        list of the modules
            SK_title:           title of the application "Skeleton Key"

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

    def module_manager_demo(self):
        # Andrew needs to fix this but this basically it
        self.module_manager = ModuleManager()
        print(*self.module_manager.module_list, sep=", ")

    def __init__(self, module_list, debug=False):
        super().__init__(debug=debug)

        self.module_list = module_list

        self.SK_title = "'Skeleton Key Project'"

    def display_title(self):
        print(self.SK_title)

    def display_modules(self):
        if not self.module_list:
            raise ValueError("There are no modules to display.")
        else:
            x = 1
            for module in self.module_list:
                print(x, " ", module)
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
                raise ValueError("Invalid selection - string instead of integer.")
                pass
            elif user_selection < 0 or user_selection > len(self.module_list):
                raise ValueError("Invalid index selection. Please enter a valid selection.")
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

    def __exit__(self):
        print("Killing Interface...")
        # if component interface is unresponsive this method provides a kill switch
        for file in self.files:
            os.unlink(file)


# debugging
if __name__ == '__main__':
    test_file = ["Responder", "NMap", "Enumeration"]
    # intro = InterfaceObject(module_list=test_file)
    with InterfaceObject(module_list=test_file) as intro:
        print(InterfaceObject.display_title(intro))
        print(InterfaceObject.display_modules(intro))
        InterfaceObject.input_choice(intro)


    test_config = configparser.Configparser()
    test_config.sections()
    test_config.read('test_config.ini')
    # not sure yet what config file we're pulling here

