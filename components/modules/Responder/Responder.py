import subprocess

from components.framework.Debug import Debug
from components.framework.network import FwComponentNetwork

network = FwComponentNetwork()


class Responder(Debug):

    def capture(self):
        network.up()
        subprocess.call("python ../components/modules/Responder/src/Responder.py")
        network.down()
