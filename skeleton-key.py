import configparser
import os

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
            ui.debug("Error: " + self.module_path + " directory does not exist!")

        # if no modules present exit
        if not self.module_list:
            ui.debug("Error: No modules found!")
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

        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = self.main_path + "/modules/"

