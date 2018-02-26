class Debug(object):
    """The base class for all components"""

    def __init__(self, name="debug", type="component", debug=False):
        self._debug = debug
        self._name = name
        self._type = type
        self._operations = 0
        self._successful_operations = 0

    def __exit__(self):
        self.debug(str(self._successful_operations) + "/" + str(self._operations) + " succeeded")

    def debug(self, txt=""):
        if self._debug:
            print(self._type, '/', self._name, ': ', txt, sep="")

    def action(self, outcome=True):
        """
        :param outcome: Boolean for successful or unsuccessful action
        :return None:
        """
        self._operations += 1
        if outcome:
            self._successful_operations += 1
