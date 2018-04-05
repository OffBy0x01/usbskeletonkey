import configparser
import importlib
import os
import pickle
import subprocess

from components.framework.Debug import Debug
from components.helpers.Format import Format
from components.helpers.ModuleManager import ModuleManager


class SkeletonKey:
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

    def __init__(self, debug=""):

        # Define directory and module paths
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.config_file = self.main_path + '/config.ini'

        self.main_path += "/components"
        self.module_path = self.main_path + "/modules"


        # Load or create config files
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
            self.config.set('interface', 'debug', 'false')

            # Disable debug if not specified
            debug = False if debug == "" else debug

            # General options
            self.config.add_section('general')
            self.config.set('general', 'config_mode', 'true')
            self.config.set('general', 'pin_armed', 'false')

            with open('config.ini', 'w') as self.config_file:
                self.config.write(self.config_file)

            self.config_mode = True

        else:
            # Config file exists, start importing
            self.config.read(self.config_file)

            # Set debug state accordingly
            debug = self.config.get('interface', 'debug').lower() == "true" if debug == "" else debug

            # if no display = armed is in effect
            pin_armed = self.config.get('general', 'pin_armed').lower() == "true" and self.is_pin_armed()

            # Set current run state (config | Armed)
            self.config_mode = self.config.get('general', 'config_mode').lower() == "true" or pin_armed

        self.main = Debug(debug=debug, name="Skeleton Key", type="Main")
        self.module_manager = ModuleManager(debug=debug)
        self.module_debug = debug

        self.SK_title = ("____ _  _ ____ _    ____ ___ ____ _  _    _  _ ____ _   _ \n"
                         "[__  |_/  |___ |    |___  |  |  | |\ |    |_/  |___  \_/  \n"
                         "___] | \_ |___ |___ |___  |  |__| | \|    | \_ |___   |   \n")

        # Ensure that modules folder exists
        if not (os.path.exists(self.module_path)):
                self.main.debug("ERROR: " + self.module_path + " directory does not exist", color=Format.color_warning)


    # Check if 'pin' says go
    def is_pin_armed(self):
        output = subprocess.run(["tvservice", "-s"], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
        if output[6:14] != "0x40001" and "not found" not in output:
            return True
        return False

    # ARMED MODE
    def armed_mode(self):
        """
        Loads modules from the module load order and runs them
        """
        with open('module_load_order', 'rb') as fp:
            unpickler = pickle.Unpickler(fp)
            armed_module_list = unpickler.load()

        for this_module in armed_module_list:
            try:
                self.main.enable_module_debug(str(this_module))
                self.main.debug("~~~Start of " + str(this_module) + "~~~", color=Format.color_primary)
                imp_module = importlib.import_module("components.modules." + this_module + "." + this_module,
                                                     this_module)
            except Exception as Err:
                self.main.debug("LOAD ERROR: " + str(Err), color=Format.color_warning)
            else:
                try:
                    # This is why modules must stick to the naming convention
                    # If this_module does not have ".run" tough luck, no gonna do it pal.

                    # import config data for this module
                    current_config = self.module_manager.get_module_by_name(this_module)

                    # Module needs to be enabled before it will run
                    if current_config.options["enabled"] == "true":
                        self.main.debug(txt=str(this_module) + " is enabled", color=Format.color_success)
                        module_class = getattr(imp_module, this_module)
                        runnable = module_class(self.main_path, debug=self.module_debug)
                        runnable.run()
                    else:
                        self.main.debug(txt=str(this_module) + " is disabled", color=Format.color_danger)

                except Exception as WTF:
                    self.main.debug("RUN ERROR: " + str(WTF), color=Format.color_warning)

            self.main.debug("~~~~End of " + str(this_module) + "~~~~\n\n", color=Format.color_primary)

    def display_title(self):
        print(Format.color_danger + self.SK_title + Format.format_clear)

    def display_modules(self):
        # displays all module information.
        if not self.module_manager.module_list:
            # TODO REVIEW CAUSE OF ERROR HERE
            raise ValueError("There are no modules to display.")
        else:
            x = 1
            for module in self.module_manager.module_list:
                print(x, " ", module.module_name)
                x += 1

    def show_module_attributes(self, user_selection):
        module = self.module_manager.module_list[user_selection - 1]
        print("\nModule Name: ", module.module_name, "\n")
        print("Module Description: ", module.module_desc, "\n")
        print("Framework Requirements: ", module.fw_requirements, "\n")
        print("Options: ", module.options, "\n")
        print("Module Help: ", module.module_help, "\n")
        print("Output Format: ", module.output_format)

    def show_module_attribute(self, config_selection, user_selection):
        module = self.module_manager.module_list[user_selection - 1]
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
            print(Format.color_warning + "ERROR: Please enter a valid attribute" + Format.format_clear)

    def set_module_attribute(self, config_selection, user_selection):
        # set flag to display error message if option is invalid
        flag = False
        module = self.module_manager.module_list[user_selection - 1]
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
            print(Format.color_danger + "Exiting Module setter..." + Format.format_clear)
        else:
            print(Format.color_warning + "ERROR: Please enter a valid attribute to set" + Format.format_clear)

    def show_module_option(self, config_selection, user_selection):
        # set flag to display error message if option is invalid
        flag = False
        module = self.module_manager.module_list[user_selection - 1]
        # if option[key] is equal to the second word

        for x in module.options:
            if config_selection[1] == "option" and x == config_selection[2]:
                print(x, " : ", module.options[x])
                flag = True
        if not flag:
            print(Format.color_warning + "ERROR: Please enter a valid option to show" + Format.format_clear)

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
        print("order				            - allows user to alter module load order")
        print("ONCE IN MODULE LOADER:")
        print("         module [module index] up		            - moves module up 1")
        print("         module [module index] down		            - moves module down 1")
        print("         module [module index] [index]		        - moves module to index")
        print("\n")
        print("save 				            - saves config")
        print("help 				            - provides helpful commands")
        print("exit 				            - exits configuration mode")
        print("\n")
        print("Leaving help...")
        return



    def save_module_config(self, config_selection, user_choice):
        print("Confirm action: (Y/N)")
        print(Format.color_warning + "color_warning: Any unsaved changes will be lost on exit" + Format.format_clear)
        module = self.module_manager.module_list[user_choice - 1]
        confirm_save = input(Format.color_primary + "%s/%s/%s>" % ("Configure", module.module_name, "Save") + Format.format_clear)
        confirm_save = confirm_save.upper()
        if confirm_save == "Y":
            print(Format.color_success + "Changes saved" + Format.format_clear)
            self.module_manager.save_config(module.module_name, True)

            self.module_manager.update_order(module.module_name)

        elif confirm_save == "N":
            print("Discarding changes...")

    def move_module_by(self, module_index, move_to):
        try:
            self.main.debug("Move %s from #%s to #%s" % (self.module_manager.module_order[module_index], module_index, move_to), color=Format.color_info)
            temporary_holder = self.module_manager.module_order[module_index]
            self.module_manager.module_order.remove(self.module_manager.module_order[module_index])
            self.module_manager.module_order.insert(move_to, temporary_holder)
        except Exception:
            print(Format.color_warning + "Please enter a valid command" + Format.format_clear)

    def update_module_order(self):
        # PICKLE
        with open('module_load_order', 'wb') as fp:
            modules_to_pickle = [mod for mod in self.module_manager.module_order]
            pickle.dump(modules_to_pickle, fp)

    def edit_module_order(self, user_choice):
        print("Use the following commands to change the module load order")
        print("order [module index] [order placement]")
        print("order [module index] up")
        print("order [module index] down")
        try:
            change_order_command = str(input(Format.color_primary + "%s/%s/Order>" % ("Configure", self.module_manager.module_order[user_choice - 1]) + Format.format_clear)).lower().split()
        except Exception:
            print(Format.color_warning + "Please enter a valid command" + Format.format_clear)
        if len(change_order_command) is not 3:
            print(Format.color_warning + "Please enter a valid command" + Format.format_clear)
        else:
            if change_order_command[0] == "order":
                try:
                    current_index = int(change_order_command[1])
                except ValueError:
                    print(Format.color_warning + "Invalid Module index" + Format.format_clear)
                if change_order_command[2] == "up":
                    # move item up 1
                    self.move_module_by(current_index, (current_index - 1))
                elif change_order_command[2] == "down":
                    self.move_module_by(current_index, (current_index + 1))
                else:
                    check = self.check_order_is_number(change_order_command[2])
                    if(check):
                        if int(change_order_command[2]) < len(self.module_manager.module_list):
                            self.move_module_by(int(change_order_command[1]), (int(change_order_command[2])))
                        else:
                            print(Format.color_warning + "Integer out of range" + Format.format_clear)
                    else:
                        print(Format.color_warning + "Please enter a valid command" + Format.format_clear)
        # Implement potential changes
        self.update_module_order()

    @staticmethod
    def check_order_is_number(test_case):
        try:
            int(test_case)
            return True
        except ValueError:
            return False

    def edit_module_order_question(self, user_choice):  # TODO Check this
        print("Current module order")
        if not self.module_manager.module_order:
            print("There are currently no modules enabled")
        else:
            for index in range(len(self.module_manager.module_order)):
                print(index, self.module_manager.module_order[index])
        try:
            change_order = input("Change module order? (Y/N)")
        except ValueError:
            print(Format.color_warning + "Please enter a valid input" + Format.format_clear)
        change_order = change_order.upper()
        if change_order == "Y":
            self.edit_module_order(user_choice)

        elif change_order == "N":
            pass
        else:
            print("Invalid response entered. Please try again.")

    def module_configuration(self, user_choice):
        # mainly for debug
        # RETURN current_module (move to current_module file)
        print("Entering Configuration mode")
        config_mode = True
        save_flag = False
        while config_mode:
            print("Enter 'exit' to finish.")
            print("\n")

            # Whatever the user enters - convert it to lowercase and place each word in an array.
            config_selection = str(input(Format.color_primary + "Configure/%s>" % self.module_manager.module_list[user_choice - 1].module_name + Format.format_clear)).lower().split()
            if len(config_selection) == 0:
                print("Please enter a valid command")
                self.display_help()
            else:
            # If the users enters one word - i.e. a keyword such as 'show', 'set' or 'exit' run
                if len(config_selection) == 1:
                    if config_selection[0] == "exit":
                        if not save_flag:
                            try:
                                confirm_exit = input(Format.color_warning + "You are about to exit without saving, are you sure? (Y/N)" + Format.format_clear)
                            except ValueError:
                                print(Format.color_warning + "Please enter a valid input" + Format.format_clear)
                            confirm_exit = confirm_exit.upper()
                            if confirm_exit == "Y":
                                print(Format.color_danger + "Exiting Configuration mode..." + Format.format_clear)
                                config_mode = False
                                pass
                            elif confirm_exit == "N":
                                pass
                        elif save_flag:
                            print(Format.color_danger + "Exiting Configuration mode..." + Format.format_clear)
                            config_mode = False
                            pass
                    elif config_selection[0] == "show":
                        # display all information to do with current module.
                        self.show_module_attributes(user_choice)
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
                        self.save_module_config(config_selection, user_choice)
                        save_flag = True
                        pass
                    elif config_selection[0] == "order":
                        self.edit_module_order_question(user_choice)
                        pass
                    else:
                        print("Please enter a valid keyword.")
                # If the users enters two words - i.e. a keyword such as 'show name' or 'set rhosts'
                elif len(config_selection) == 2:
                    if config_selection[0] == "show":
                        # run method to show selected attribute
                        self.show_module_attribute(config_selection, user_choice)
                        pass
                    elif config_selection[0] == "set":
                        # run method to set selected attribute
                        self.set_module_attribute(config_selection, user_choice)
                        pass
                    else:
                        print("Please enter a valid command")
                elif len(config_selection) == 3:
                    if config_selection[0] == 'set':
                        # run method to set selected attribute
                        self.set_module_attribute(config_selection, user_choice)
                        pass
                elif config_selection[0] == 'show':
                    self.show_module_option(config_selection, user_choice)
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
            print(Format.color_info + "Enter 0 to exit" + Format.format_clear)
            try:
                user_selection = int(input("Please enter the module you would like to configure. (Based on index)"))
            except ValueError:
                print(Format.color_warning + "ERROR: Invalid selection - string instead of integer." + Format.format_clear)
                return -1
            else:
                # Based on user input - moves to respective method
                if user_selection == 0:
                    print(Format.color_danger + "Exiting Program..." + Format.format_clear)
                    exit_flag = True

                    # Implement potential order changes
                    self.update_module_order()

                    return user_selection
                elif user_selection < 0 or user_selection > len(self.module_manager.module_list):
                    print(Format.color_warning + "ERROR: Invalid index selection. Please enter a valid selection." + Format.format_clear)
                else:
                    if not exit_flag:
                        return user_selection
                    else:
                        # Ending program
                        print(Format.color_success + "Thank you for using 'Skeleton Key'." + Format.format_clear)
                        exit(0)

    @staticmethod
    def yorn(output, expected):
        """
        Yes or No style query

        Example:
        >>>if self.yorn("Please say Y? (Y/N)", "Y"):
        >>>  print("entered Y")
        >>>else:
        >>>  print("You didn't enter Y")

        :param output: What to ask the user and waiting for a response
        :param expected: A string that should match your yes case

        :return: Boolean did response match expected user input
        """
        response = input(output).__str__().strip()

        if response.upper() == expected.upper():
            return True

        return False

    def run(self):
        if self.config_mode:
            # Config mode
            self.main.debug("Entering Config Mode", color=Format.color_warning)
            selection = -1
            while selection != 0:
                selection = self.input_choice()
                if 1 <= selection <= 9999999:
                    self.module_configuration(selection)
        else:
            # Armed mode
            self.main.debug("Entering Armed Mode", color=Format.color_warning)
            self.armed_mode()



    def __exit__(self):
        print("Killing Interface...")
        # if component interface is unresponsive this method provides a kill switch
        for file in self.files:
            os.unlink(file)


# TODO #ATSOMEPOINT implement new testing methods

if __name__ == '__main__':
    skeleton_key = SkeletonKey()
    skeleton_key.run()
