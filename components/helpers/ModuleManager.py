import configparser
import os
from pathlib import Path

from components.framework.Debug import Debug
from components.helpers.Format import Format
from components.helpers.ModuleDescriptor import ModuleDescriptor


class ModuleManager:
    """
     Args:
                save_needs_confirm          Flag to determine if the manager should rely on the confirmation state or
                                            just allow all save attempts

                debug                       Flag to enable or disable debug messages which can provide further feedback
                                            on status of module

            functions:
                get_module_by_name          Returns the module descriptor of a module specified by name

                save_config                 Saves the current configuration of a module specified by name

                import_module_config        Imports the configuration file of all modules, overwrites unsaved
                                            module configurations

            Returns:
                ModuleManager object

            Raises:
                A dog


    """
    def __init__(self, debug=False, save_needs_confirm=True):
        self.module_manager = Debug(name="ModuleManager", type="Helper", debug=debug)

        # Enables or disables the save confirmation feature
        self.save_needs_confirm = save_needs_confirm

        # Define directory and module paths
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.modules_dir = self.main_path + "/../modules"
        self.module_list = []
        self.module_order = []
        self.import_module_configs()

    def get_module_by_name(self, module):
        for m in self.module_list:
            if m.module_name == module:
                return m
        self.module_manager.debug("Error: Unable to get module by name: %s" % module, color=Format.color_danger)

    def save_config(self, module_name, confirm=False):
        """
        Saves current module config to the appropriate ini file

        :param module_name:
        :param confirm:
        :return True if success, False if Failure:
        """

        # Saves current configuration to module config file
        if confirm or not self.save_needs_confirm:
            config = configparser.ConfigParser()
            module_config = self.modules_dir + '/%s/%s.ini' % (module_name, module_name)
            config.read(module_config)
            # locate module that will be editing
            module = self.get_module_by_name(module=module_name)

            config.set("general", "module_name", module.module_name)
            config.set("general", "module_desc", module.module_desc)
            config.set("general", "version", module.version)
            config.set("general", "module_help", module.module_help)
            for option in module.options.items():
                self.module_manager.debug("option: " + option[0] + " : " + option[1], color=Format.format_clear)
                config.set("options", option[0], option[1])
            for fw_requirements in module.fw_requirements.items():
                config.set("fw_requirements", fw_requirements[0], fw_requirements[1])
            for output_format in module.output_format.items():
                config.set("output_format", output_format[0], output_format[1])

            with open(module_config, 'w') as configfile:
                config.write(configfile)
            self.module_manager.debug("Saved module options", color=Format.color_success)

            return True
        return False

    def discover_modules(self):
        """
        looks for modules where modules are a directory containing files
        There should be at least one .py file -but if not that's not our fault.

        :return modules as list:
        """

        # get the module paths from modules directory
        self.module_manager.debug("discover_modules: Looking for modules...", color=Format.color_info, formatting=Format.decoration_bold)
        module_paths = os.listdir(self.modules_dir)

        # identify module name from file path
        #        return [os.path.splitext(m)[0] for m in module_paths]
        return [m for m in module_paths if os.path.isdir(self.modules_dir + "/" + m)]

    def import_module_configs(self):
        # print("Import Module Configs:")
        config = configparser.ConfigParser()

        # (Import | Freak out over) module config
        for this_module in self.discover_modules():

            module_path = self.modules_dir + '/%s/%s.ini' % (this_module, this_module)

            try:
                # Attempt to read current module's config file
                Path(module_path).resolve()

            except FileNotFoundError:

                # Was unable to read this module, log an error then skip
                self.module_manager.debug(this_module + " config file not found!", color=Format.color_warning)
                self.module_manager.debug(module_path)
                continue

            else:
                # Module config exists, start importing datas
                self.module_manager.debug(this_module + " config file found, importing data", color=Format.format_clear)
                config.read(module_path)

            try:
                # get  module_desc, options, fw_requirements, output_format, version, module_help
                current_module = ModuleDescriptor(
                    module_name=config.get("general", 'module_name'),
                    module_desc=config.get("general", 'module_desc'),
                    version=config.get("general", 'version'),
                    module_help=config.get("general", 'module_help'),
                    # _sections[section] returns as a dictionary
                    options=config._sections['options'],
                    fw_requirements=config._sections['fw_requirements'],
                    output_format=config._sections['output_format']
                )
                self.module_list.append(current_module)

                # Prevent ordered dict from duplicating everything
                config._sections["general"] = {}
                config._sections["options"] = {}
                config._sections["fw_requirements"] = {}
                config._sections['output_format'] = {}

            except configparser.Error:
                self.module_manager.debug("Error: Unable to import module from file", color=Format.color_warning)
            else:
                self.update_order(module_name=this_module)

        self.module_manager.debug("modules loaded: " + str([module.module_name for module in self.module_list]), color=Format.color_info if len(self.module_list) else Format.color_danger)

    def update_order(self, module_name):
        try:
            module = self.get_module_by_name(module_name)

            if "true" == module.options["enabled"].lower():
                try:
                    # If it already exists it needs to be removed first
                    self.module_order.remove(module_name)
                except Exception:
                    # Easier to ask for forgiveness
                    pass

                # Add module to order
                self.module_order.append(module_name)
                self.module_manager.debug("%s added to order" % (module_name), color=Format.color_info)


            else:
                try:
                    self.module_order.remove(module_name)
                except Exception:
                    pass  # probably don't need to remove it
                else:
                    self.module_manager.debug("% removed from order", color=Format.color_success)
        except Exception as reason:
            self.module_manager.debug("Could not add or remove %s as %s" % (module_name, reason), color=Format.color_warning)
