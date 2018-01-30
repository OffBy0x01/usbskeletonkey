import configparser
import os
import re
from pathlib import Path

from framework.FwComponent import FwComponent
from framework.helper.ModuleDescriptor import ModuleDescriptor


class SkeletonKey(object):
    # TODO update descriptor
    """
       Class for the Interface

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

    def __init__(self, debug=False):
        # Hack for network config (something ellis has placed in - its causing errors just now) TODO: Fix this code
        # subprocess.call("cp dhcpd.conf /etc/dhcp/dhcpd.conf", shell=True)
        # subprocess.call("echo -e 'iface usb0 inet static\naddress 10.10.10.10\nnetmask 128.0.0.0\ngateway 10.10.10.1' >> /etc/network/interfaces", shell=True)

        self.SK_title = ("____ _  _ ____ _    ____ ___ ____ _  _    _  _ ____ _   _ \n"
                         "[__  |_/  |___ |    |___  |  |  | |\ |    |_/  |___  \_/  \n"
                         "___] | \_ |___ |___ |___  |  |__| | \|    | \_ |___   |   \n")

        self.module_list = []
        self.fw_debug = FwComponent(debug=debug)

        # Define directory and module paths
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = self.main_path + "/modules"
        self.config_file = self.main_path + '/config.ini'
        # Ensure that modules folder exists
        if not (os.path.exists(self.module_path)):
            self.fw_debug.debug("Error: " + self.module_path + " directory does not exist")

        # Get module names from file - no data ported yet
        self.raw_module_list = self.discover_modules()
        if not self.raw_module_list:
            self.fw_debug.debug("Error: No modules found!")
        else:
            self.fw_debug.debug(*self.raw_module_list)

        # TODO #3 clean up config parser calls
        '''Load or create config files'''
        self.config = configparser.ConfigParser()

        # (Import | Create) default config
        try:
            # Attempt to read config
            open(self.config_file)
        except FileNotFoundError:
            # Config not found, set defaults
            self.config.read(self.config_file)

            # Interface options
            self.config.add_section('interface')
            self.config.set('interface', 'debug', 'False')

            # General options
            self.config.add_section('general')
            self.config.set('general', 'config_mode', 'True')
            self.config_mode = True
        else:
            # Config file exists, start importing
            self.config.read(self.config_file)

            # Set debug state accordingly
            if self.config.get('interface', 'debug') == "True":
                self.debug = True
            else:
                self.debug = False

            # Set current run state (config | Armed)
            if self.config.get('general', 'config_mode') == "True":
                self.config_mode = True
            else:
                self.config_mode = False

        with open('config.ini', 'w') as self.config_file:
            self.config.write(self.config_file)

        self.config = configparser.ConfigParser()

        # (Import | Freak out over) module configs
        for module in self.raw_module_list:

            self.module_config = self.module_path + '/%s.ini' % module

            try:
                # Attempt to read current module's config file
                self.fw_debug.debug(self.module_config)
                Path(self.module_config).resolve()

            except FileNotFoundError:

                # Was unable to read this module, log an error then skip
                self.fw_debug.debug(module + " config file not found!")
                continue

            else:
                # Module config exists, start importing datas
                self.fw_debug.debug(module + " config file found, importing data")
                self.config.read(self.module_config)

            try:

                # get  module_desc, options, fw_requirements, output_format, version, module_help
                current_module = ModuleDescriptor(
                    module_name=self.config.get(module, 'module_name'),
                    module_desc=self.config.get(module, 'module_desc'),
                    version=self.config.get(module, 'version'),
                    module_help=self.config.get(module, 'module_help'),
                    # _sections[section] returns as a dictionary
                    options=self.config._sections['options'],
                    fw_requirements=self.config._sections['fw_requirements'],
                    output_format=self.config._sections['output_format']
                )
                self.module_list.append(current_module)

            except configparser.Error:
                self.fw_debug.debug("Error: Unable to import module from file")
                pass
            else:
                self.fw_debug.debug("modules loaded:")
                self.fw_debug.debug(*[module.module_name for module in self.module_list])
        # TODO WORK OUT WHAT HAPPENS IN ARMED MODE

    def discover_modules(self):
        # get the module paths from modules directory
        print("Looking for modules...")
        module_paths = os.listdir(self.module_path)

        # regex to look for .py files
        py = re.compile("\.py", re.IGNORECASE)
        module_paths = filter(py.search, module_paths)

        # identify module name from file path
        return [os.path.splitext(m)[0] for m in module_paths]

    def display_title(self):
        # displays title
        print(self.SK_title)

    def display_modules(self):
        # displays all module information.
        if not self.module_list:
            # TODO REVIEW CAUSE OF ERROR HERE
            raise ValueError("There are no modules to display.")
        else:
            x = 1
            for module in self.module_list:
                print(x, " ", module.module_name)
                x += 1

    def display_information_current_module(self, user_selection):
        module = self.module_list[user_selection - 1]
        print("Module Name: ", module.module_name)
        print("Module Description: ", module.module_desc)
        print("Framework Requirements: ", module.fw_requirements)
        print("Options: ", module.options)
        print("Module Help: ", module.module_help)
        print("Output Format: ", module.output_format)

    # TODO review if need this
    def bool_ask_question(self, question):
        """ Desc:
                Enables asking of y/n questions"""

    # TODO 1: Review how to fix this
    def show_with_att(self, config_selection, user_selection):
        module = self.module_list[user_selection - 1]
        if "name" in config_selection[1]:
            print("Module Name: ", module.module_name)
        elif "desc" in config_selection[1]:
            print("Module Description: ", module.module_desc)
        elif "req" in config_selection[1]:
            print("Framework Requirements: ", module.fw_requirements)
        elif "opt" in config_selection[1]:
            print("Options: ", module.options)
        elif "help" in config_selection[1]:
            print("Module Help: ", module.module_help)
        elif "format" in config_selection[1]:
            print("Output Format: ", module.output_format)
        else:
            print("Please enter a valid attribute")

    # TODO 2: test this method for bugs
    def set_with_att(self, config_selection, user_selection):
        # set flag to display error message if option is invalid
        set = False
        module = self.module_list[user_selection - 1]
        # if option[key] is equal to the second word

        for x in module.options:
            if x == config_selection[1]:
                new_value = input("Enter the value you would like to set this to")
                module.options[config_selection[1]] = new_value
                set = True
            else:
                pass
        if set:
            pass
        else:
            print("Please enter a valid attribute to set")
        pass

    def module_configuration(self, user_choice):
        # mainly for debug
        # RETURN current_module (move to current_module file)
        print("Entering Configuration mode")
        config_mode = True
        while config_mode:
            print("Enter 'exit' to finish.")
            print("\n")

            # Whatever the user enters - convert it to lowercase and place each word in an array.
            config_selection = str(input(">")).lower().split()

            # If the users enters one word - i.e. a keyword such as 'show', 'set' or 'exit' run
            if len(config_selection) == 1:
                if config_selection[0] == "exit":
                    print("Exiting Configuration mode...")
                    config_mode = False
                    pass
                elif config_selection[0] == "show":
                    # display all information to do with current module.
                    self.display_information_current_module(user_choice)
                    pass
                elif config_selection[0] == "set":
                    print("Please select an attribute to set in the format 'set [attribute]'")
                    # provide options on what is available to set
                    pass
            # If the users enters two words - i.e. a keyword such as 'show name' or 'set rhosts'
            elif len(config_selection) == 2:
                if config_selection[0] == "show":
                    # run method to show selected attribute
                    self.show_with_att(config_selection, user_choice)
                    pass
                elif config_selection[0] == "set":
                    # run method to set selected attribute
                    self.set_with_att(config_selection, user_choice)
                    pass
            else:
                print("wtf")
                pass

    # Main menu for Interface, takes user input of which module they would like to use
    def input_choice(self):
        # exit flag for ending the program
        exit_flag = False
        while not exit_flag:
            # Display title
            self.display_title()
            # Display modules
            self.display_modules()

            # Communicating to user how to use the Interface.
            print("\n")
            print("Enter 0 to exit")
            user_selection = int(input("Please enter the module you would like to configure. (Based on index)"))

            # Based on user input - moves to respective method
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
                    return user_selection
                else:
                    # Ending program
                    print("Thank you for using 'Skeleton Key'.")
                    exit(0)

    def __exit__(self):
        print("Killing Interface...")
        # if component interface is unresponsive this method provides a kill switch
        for file in self.files:
            os.unlink(file)


# TODO #ATSOMEPOINT implement new testing methods


# debugging
if __name__ == '__main__':
    begin = SkeletonKey(debug=True)
    begin.display_title()
    begin.display_modules()
    selection = begin.input_choice()
    begin.module_configuration(selection)
