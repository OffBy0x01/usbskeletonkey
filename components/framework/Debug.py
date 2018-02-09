class Debug(object):
    """The base class for all components"""

    def __init__(self, name="debug", type="component", debug=False):
        self._debug = debug
        self._name = name
        self._type = type

    def debug(self, txt=""):
        if self._debug:
            print(self._type, '/', self._name, ': ', txt, sep="")
