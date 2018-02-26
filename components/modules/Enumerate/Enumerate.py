from components.framework.Debug import Debug
from components.helpers.ModuleManager import ModuleManager


class TargetInfo:
    def __init__(self):
        self.OS_INFO = []
        self.SOFTWARE_INFO = []
        self.WORKGROUP = []
        self.DOMAIN = []  # USERS + GROUPS
        self.LOCAL = []  # USERS + GROUPS
        self.SESSIONS = []
        self.NBT_STAT = []
        self.SHARE_INFO = []  # include SMB info?
        self.PASSWD_POLICY = []
        self.PRINTER_INFO = []
        self.PORTS = {}  # prolly formatted like this "PORT_NUMBER : STATUS"


class Enumerate(Debug):
    def __init__(self, debug=False):
        super().__init__(name="Enumerate", type="Module", debug=debug)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name("Enumerate")

    def run(self):
        pass

    # Extracting the information we need is going to look disguisting, try to keep each tool in a single def.
    # e.g. def for nbtstat, def for nmap, def for net etc...


e = Enumerate()
