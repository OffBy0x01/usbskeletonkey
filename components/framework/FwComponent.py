class FwComponent(object):
    """The base class for all components"""

    def __init__(self, debug=False):
        self._debug = debug

    def debug(self, txt=""):
        if self._debug:
            print(txt)
