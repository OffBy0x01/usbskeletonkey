import configparser
import os

from components.framework.Debug import Debug
from components.helpers.ModuleManager import ModuleManager


class SkeletonKey(ModuleManager, Debug):
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
        super().__init__(debug=debug)
        # Hack for network config (something ellis has placed in - its causing errors just now) TODO: Fix this code
        # subprocess.call("cp dhcpd.conf /etc/dhcp/dhcpd.conf", shell=True)
        # subprocess.call("echo -e 'iface usb0 inet static\naddress 10.10.10.10\nnetmask 128.0.0.0\ngateway 10.10.10.1' >> /etc/network/interfaces", shell=True)

        self.SK_title = ("____ _  _ ____ _    ____ ___ ____ _  _    _  _ ____ _   _ \n"
                         "[__  |_/  |___ |    |___  |  |  | |\ |    |_/  |___  \_/  \n"
                         "___] | \_ |___ |___ |___  |  |__| | \|    | \_ |___   |   \n")

        # Define directory and module paths
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = self.main_path + "/modules"
        self.config_file = self.main_path + '/config.ini'

        # Ensure that modules folder exists
        if not (os.path.exists(self.module_path)):
            self.debug("ERROR: " + self.module_path + " directory does not exist")

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

        # TODO WORK OUT WHAT HAPPENS IN ARMED MODE

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
            print("ERROR: Please enter a valid attribute")

    def set_with_att(self, config_selection, user_selection):
        # set flag to display error message if option is invalid
        flag = False
        module = self.module_list[user_selection - 1]
        # if option[key] is equal to the second word

        for x in module.options:
            if x == config_selection[1]:
                if len(config_selection) == 3:
                    module.options[config_selection[1]] = str(config_selection[2])
                    flag = True
                else:
                    new_value = input("Enter the value you would like to set this to")
                    module.options[config_selection[1]] = new_value
                    flag = True
        if flag:
            print("Value changed")
        else:
            print("ERROR: Please enter a valid attribute to set")

    def show_select_option(self, config_selection, user_selection):
        # set flag to display error message if option is invalid
        flag = False
        module = self.module_list[user_selection - 1]
        # if option[key] is equal to the second word

        for x in module.options:
            if config_selection[1] == "option" and x == config_selection[2]:
                print(x, " : ", module.options[x])
                flag = True
        if flag:
            pass
        else:
            print("ERROR: Please enter a valid option to show")
            pass

    def display_help(self):
        # Displays help information for Skeleton Key
        print("Displaying help...")
        print("\n")
        print("Command                          Description of command")
        print(
            "--------------------------------------------------------------------------------------------------------------------")
        print("show				            - shows all info on the current module")
        print("show [attribute]		        - shows the info on the specified attribute of the current module")
        print("set				                - displays instructions on how to use the set command")
        print(
            "set [attribute]			        - allows the user to enter a value to set the specified attribute for the current module")
        print("set [attribute] [value]		    - sets the value for the specified attribute for the current module")
        print("exit 				            - exits configuration mode")
        print("\n")
        print("Leaving help...")
        return

    def user_save(self, config_selection, user_choice):
        print("Confirm action: (Y/N)")
        print("WARNING: Any unsaved changes will be lost on exit")
        confirm_save = input(">")
        confirm_save = confirm_save.upper()
        module = self.module_list[user_choice - 1]
        module_name = module.module_name
        if confirm_save == "Y":
            print("Saving...")
            self.save_config(module_name, True)
            pass
        elif confirm_save == "N":
            print("Discarding changes...")
            self.save_config(module_name, False)
            pass

    def move_module_by(self, module_index, move_to):
        #temporary_holder = []
        temporary_holder = self.module_list[module_index]
        self.module_list.remove(self.module_list[module_index])
        self.module_list.insert(move_to, temporary_holder)

    def change_module_order(self, user_choice):
        print("Use the following commands to change the module load order")
        print("order [module index] [order placement]")
        print("order [module index] up")
        print("order [module index] down")
        try:
            change_order_command = str(input(">")).lower().split()
        except ValueError:
            print("Please enter a valid command")
        if len(change_order_command) is not 3:
            print("Please enter a valid command")
        elif len(change_order_command) is 3:
            if change_order_command[0] == "order":
                try:
                    current_index = int(change_order_command[1])
                except ValueError:
                    print("Module index is not in list")
                if change_order_command[2] == "up":
                    #move item up 1
                    self.move_module_by(current_index, (current_index - 1))
                    pass
                elif change_order_command[2] == "down":
                    self.move_module_by(current_index, (current_index + 1))
                    pass
                elif int(change_order_command[2]) >= 0:
                    if int(change_order_command[2]) < len(self.module_list):
                        self.move_module_by(int(change_order_command[1]), (int(change_order_command[2])))
                    else:
                        print("Integer out of range")
                    pass
                else:
                    print("Please enter a valid command")
            else:
                print("Please enter a valid command")

    def show_module_order(self, user_choice):
        print("Current module order")
        if self.module_order == 0:
            print("There are currently no modules in line")
        else:
            for x in range(0, len(self.module_order)):
                module = self.module_list[x]
                print(x, " ", module.module_name)
        try:
            change_order = input("Change module order? (Y/N)")
        except ValueError:
            print("Please enter a valid input")
        change_order = change_order.upper()
        if change_order == "Y":
            self.change_module_order(user_choice)
            pass
        elif change_order == "N":
            pass
        else:
            print("Invalid response entered. Please try again.")

    def module_configuration(self, user_choice):
        # mainly for debug
        # RETURN current_module (move to current_module file)
        self.module_order.append(user_choice)
        print("Entering Configuration mode")
        config_mode = True
        save_flag = False
        while config_mode:
            print("Enter 'exit' to finish.")
            print("\n")

            # Whatever the user enters - convert it to lowercase and place each word in an array.
            config_selection = str(input(">")).lower().split()

            # If the users enters one word - i.e. a keyword such as 'show', 'set' or 'exit' run
            if len(config_selection) == 1:
                if config_selection[0] == "exit":
                    if not save_flag:
                        try:
                            confirm_exit = input("You are about to exit without saving, are you sure? (Y/N)")
                        except ValueError:
                            print("Please enter a valid input")
                        confirm_exit = confirm_exit.upper()
                        if confirm_exit == "Y":
                            print("Exiting Configuration mode...")
                            config_mode = False
                            pass
                        elif confirm_exit == "N":
                            print("Ready to save.")
                            self.user_save(config_selection, user_choice)
                            print("Exiting Configuration mode...")
                            config_mode = False
                            pass
                    elif save_flag:
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
                elif config_selection[0] == "help":
                    # run method to set selected attribute
                    self.display_help()
                    pass
                elif config_selection[0] == "save":
                    # run method to set selected attribute
                    self.user_save(config_selection, user_choice)
                    save_flag = True
                    pass
                elif config_selection[0] == "order":
                    self.show_module_order(user_choice)
                    pass
                else:
                    print("Please enter a valid keyword.")
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
                    print("Please enter a valid command")
            elif len(config_selection) == 3:
                if config_selection[0] == 'set':
                    # run method to set selected attribute
                    self.set_with_att(config_selection, user_choice)
                    pass
            elif config_selection[0] == 'show':
                self.show_select_option(config_selection, user_choice)
                pass
            else:
                print("Please enter a valid command.")

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
            try:
                user_selection = int(input("Please enter the module you would like to configure. (Based on index)"))
            except ValueError:
                print("ERROR: Invalid selection - string instead of integer.")
                return -1
            else:
                # Based on user input - moves to respective method
                if user_selection == 0:
                    print("Exiting Program...")
                    exit_flag = True
                    return user_selection
                    pass
                elif user_selection < 0 or user_selection > len(self.module_list):
                    print("ERROR: Invalid index selection. Please enter a valid selection.")
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
    selection = -1
    begin = SkeletonKey(debug=True)
    while selection == -1:
        selection = begin.input_choice()
        if selection == 0:
            print("Thanks for playing.")
            break
        else:
            begin.module_configuration(selection)
            selection = -1
