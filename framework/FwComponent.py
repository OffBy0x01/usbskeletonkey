class FwComponent(object):
    """The base class for all components"""

    def debug(self, txt=""):
        if self.debug:
            print(txt)
