from components.framework.Debug import Debug
from components.framework.keyboard import Keyboard
from components.helpers.Format import Format
from components.helpers.ModuleManager import ModuleManager


# TODO: Update Doc String and comments


class KeyInject:
    """ Class for Responder Module
                Args:
               functions:
                   capture              Run Spiderlabs' Responder on usb0 so password hashes can potentially
                                        be obtained.
                   network.up           Calls a method from the framework component "network.py" that enables usb0,
                                        configures the DHCP server and IP routing for network traffic
                                        capture.
                   monitor_responder    Monitors "Responder.db" for file changes and returns when either the "time
                                        to live" period has been reached or a password hash has been captured.
                   process.kill         Kills the instance of Responder that has been running.
                   network.down         Calls a method from the framework component "network.py" that disables usb0,
                                        the DHCP server and removes IP routing for the interface.
               Returns:
                   boolean
               Raises:
           """

    # Constructor
    def __init__(self, path, debug):
        self._type = "Module"
        self._name = "KeyInject"
        self.dbg = debug

        # setup debug
        self.path = path
        self.keyinject = Debug(name=self._name, type=self._type, debug=debug)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # Import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)

        # List of scripts to execute
        scripts_to_execute = self.current_config.options["scripts"].replace(" ", "").split(',')

        # Make it known
        self.keyinject.debug("Initializing KeyInject...", color=Format.color_info)

        self.scripts = []
        for script in scripts_to_execute:
            try:
                with open("%s/modules/%s/scripts/%s" % (self.path, self._name, script)) as current_script:
                    self.scripts.append(current_script)
            except Exception as err:
                self.keyinject.debug("Error: %s" % err, color=Format.color_warning)

    # Run method for Armed mode
    def run(self):

        # Initialize keyboard fw module here it will also destroy here
        keyboard = Keyboard(debug=self.dbg, enabled=True)

        # Can't run if no scripts
        if not self.scripts:
            self.keyinject.debug("Critical: No valid scripts", color=Format.color_danger)
            return False

        self.keyinject.debug("Running KeyInject...", color=Format.format_clear)

        # Run previously specified scripts
        for script in self.scripts:
            keyboard.resolve_script(script=script)
