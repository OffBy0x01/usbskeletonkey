import subprocess

from components.framework.Debug import Debug
from components.framework.network import FwComponentNetwork

network = FwComponentNetwork


class Responder(Debug):
    # def __init__(self, debug=False):

    def up(self):
        network.up()
        self.debug(subprocess.call("python2 src/Responder.py", shell=True))
        network.down()
