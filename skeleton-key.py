import configparser
import os
import re

from framework import interface


class SkeletonKey:
    # done for tonight boiz
    def __init__(self):
        ui = interface.InterfaceObject()
        '''
        #initialize framework components
       
        keyboard = framework.keyboard()
        network = framework.network()
        storage = framework.storage()
        io = framework.io()
        '''
        # init config
        if not (os.path.exists(self.module_path)):
            # doesn't exist - user can fix themselves
            print("Error: " + self.module_path + " directory does not exist!")
            exit()

        # if no modules present exit
        if not self.module_list:
            print("Error: No modules found!")
            exit()
        else:
            print('Configuring modules:')
            print(*self.module_list, sep=',\n')

        # generate configuration file and add the required sections
        config = configparser.ConfigParser()
        config.read(self.main_path + '/config.ini')
        config.add_section('components')
        config.add_section('modules')
        config.add_section('interface')
        config.add_section('general')

        # add to modules to config.ini:active_modules
        for mod in self.module_list:
            config.set('modules', mod, "True")

        with open(self.main_path + '/config.ini', 'w') as f:
            config.write(f)

        self.module_list = self.discover_modules()
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = self.main_path + "/modules/"

    def discover_modules(self):
        # get the module paths from modules directory
        print("Looking for modules...")
        module_paths = os.listdir(self.module_path)

        # regex to look for .py files
        py = re.compile("\.py", re.IGNORECASE)
        module_paths = filter(py.search, module_paths)

        # identify module name from file path
        return [os.path.splitext(m)[0] for m in module_paths]

    def get_modules(self):
        module_list = self.discover_modules()
        return module_list
