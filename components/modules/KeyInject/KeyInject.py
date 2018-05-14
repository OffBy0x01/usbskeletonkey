from components.framework.Debug import Debug
from components.framework.keyboard import Keyboard
from components.helpers.Format import Format
from components.helpers.ModuleManager import ModuleManager

class KeyInject:
    """ Class for KeyInject Module
                Options:
		   enabled		whether this module is enabled or disabled
		   script		script or comma-seperated list of scripts to run						
               functions:
                   Run		        Run DuckyScript parser on target file 

               Returns:
                   None
               Raises:
		   IOERROR 		File could not be opened
           """

    # Constructor
    def __init__(self, path, debug):
        self.type = "Module"
        self.name = "KeyInject"
        self.dbg = debug

        # setup debug
        self.path = path
        self.keyinject = Debug(name=self.name, type=self.type, debug=debug)
        self.keyinject.debug("Debug Enabled")

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # Import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self.name)

        # List of scripts to execute
        try:
            self.scripts_to_execute = self.current_config.options["script"].split(',')
        except Exception as err:
            self.keyinject.debug("Critical Error: %s" % err, color=Format.color_danger)
        # Make it known
        self.keyinject.debug("Initializing KeyInject...", color=Format.color_info)

        self.scripts = []
        for script in self.scripts_to_execute:
            try:
                with open("%s/modules/%s/scripts/%s" % (self.path, self.name, script), "r") as current_script:
                    self.scripts.append(current_script.readlines())
            except Exception as err:
                self.keyinject.debug("Error: %s" % err, color=Format.color_warning)

    # Run method for Armed mode
    def run(self):
        self.keyinject.debug("Creating Keyboard", color=Format.color_info)
        # Initialize keyboard fw module here it will also destroy here
        keyboard = Keyboard(debug=self.dbg,path=self.path, enabled=False)
        keyboard.enable()
        # Can't run if no scripts
        if not self.scripts:
            self.keyinject.debug("Critical: No valid scripts", color=Format.color_danger)
            return False

        self.keyinject.debug("Running KeyInject...", color=Format.format_clear)

        # Run previously specified scripts
        for script in self.scripts:
            keyboard.resolve_script(script=script)
        keyboard.disable()
