import time

from components.framework.Debug import Debug
from components.framework.storage import StorageAccess
from components.helpers.ModuleManager import ModuleManager
from components.helpers.BlinktSupport import Blinkt


class Storage:
    """
    Simple module that mounts a filesystem that the user requests for a set amount of time.
    The set time allows Skeleton Key to safely shutdown upon completion

    :param debug: Simple Debug toggle. Defaults to False
    """
    def __init__(self, path, debug=False):
        name = "Storage"
        self.storage = Debug(name=name, type="Module", debug=debug)
        self.debug = debug
        self.storage.debug("Initialized")

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)
        self.storage.debug("ModuleManager Created")

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(name)
        if not self.current_config:
            self.storage.debug("Error: could not import config of " + name)

        # Import default system path

        self.file_path = self.current_config.options["file_path"].strip() + path
        self.file_name = self.current_config.options["file_name"].strip()
        self.read_only = "true" == self.current_config.options["read_only"].strip()
        self.wait = int(self.current_config.options["wait"].strip())

    def run(self):
        """
        Run function skeleton key requires.
        Opens file system on the bus, waits 45 seconds by default then closes.

        :param file_path: Path to assumed .img file e.g. /foo/bar/, ./foo/
        :param file_name: name of image file including extension e.g. bar.img
        :param read_only: Define whether to mount the file system as Read only. Defaults to False
        :param wait: How long the file system should remain mounted. Defaults to "45" seconds (Type Int)

        :return: No return
        """
        blinkt = Blinkt(200, 0, 200)

        current_storage = StorageAccess(file_name=self.file_name, file_path=self.file_path, debug=self.debug)
        current_storage.mount_bus(self.read_only)

        for tick in range(8):
            try:
                blinkt.unset_pixel(tick-1)
            finally:
                blinkt.set_pixel(tick)
                time.sleep(self.wait / 8)

        current_storage.unmount()
        return True
