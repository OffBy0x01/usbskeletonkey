import configparser
import os
from pathlib import Path

from components.framework.Debug import Debug
from components.helpers.ModuleDescriptor import ModuleDescriptor


class ModuleManager(Debug):

    def __init__(self, debug=False, save_needs_confirm=True):
        super().__init__(name="ModuleManager", type="Framework", debug=debug)

        # Enables or disables the save confirmation feature
        self.save_needs_confirm = save_needs_confirm

        # Define directory and module paths
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = self.main_path + "\..\modules"
        self.module_list = []
        self.import_module_config()

    def get_module_by_name(self, module):
        for m in self.module_list:
            if m.module_name == module:
                return m

        self.debug("Error: Unable to get module by name: " + module)

    def save_config(self, module_name, confirm=False):
        """
        Saves current module config to the appropriate ini file

        :param module:
        :param confirm:
        :return True if success, False if Failure:
        """

        # Saves current configuration to module config file
        if confirm or not self.save_needs_confirm:
            config = configparser.ConfigParser()
            module_config = self.module_path + '/%s/%s.ini' % (module_name, module_name)
            config.read(module_config)

            module = self.get_module_by_name(module=module_name)

            config.set("general", "module_name", module.module_name)
            config.set("general", "module_desc", module.module_desc)
            config.set("general", "version", module.version)
            config.set("general", "module_help", module.module_help)
            for option in module.options:
                config.set("options", option[0], option[1])
            for fw_requirements in module.fw_requirements:
                config.set("fw_requirements", fw_requirements[0], fw_requirements[1])
            for output_format in module.output_format:
                config.set("output_format", output_format[0], output_format[1])
            return True
        return False

    def discover_modules(self):
        """
        looks for modules where modules are a directory containing files
        There should be at least one .py file -but if not that's not our fault.

        :return modules as list:
        """

        # get the module paths from modules directory
        self.debug("Looking for modules...")
        module_paths = os.listdir(self.module_path)

        # identify module name from file path
        #        return [os.path.splitext(m)[0] for m in module_paths]
        return [m for m in module_paths if os.path.isdir(self.module_path + "\\" + m)]

    def import_module_config(self):
        config = configparser.ConfigParser()

        # (Import | Freak out over) module config
        for module in self.discover_modules():

            module_config = self.module_path + '/%s/%s.ini' % (module, module)

            try:
                # Attempt to read current module's config file
                self.debug(module_config)
                Path(module_config).resolve()

            except FileNotFoundError:

                # Was unable to read this module, log an error then skip
                self.debug(module + " config file not found!")
                continue

            else:
                # Module config exists, start importing datas
                self.debug(module + " config file found, importing data")
                config.read(module_config)

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

            except configparser.Error:
                self.debug("ERROR: Unable to import module from file")
            else:
                self.debug("modules loaded: " + str([module.module_name for module in self.module_list]))
