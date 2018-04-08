from components.helpers.Format import Format

class Debug(object):
    """The Debug class for all components"""

    def __init__(self, name="debug", type="component", debug=False):
        self._debug = debug
        self._name = name
        self._module = ""
        self._type = type
        self._operations = 0
        self._successful_operations = 0

    def __exit__(self):
        self.debug(str(self._successful_operations) + "/" + str(self._operations) + " succeeded")

    def debug(self, txt="", color=Format.format_clear, formatting=Format.format_clear):
        if self._debug:
            print(self._type, '/', self._name, self._module, ': ', formatting, color, txt, Format.format_clear, sep="")

    def enable_module_debug(self, module_name):
        self._module = "/" + module_name

    def disable_module_debug(self):
        self._module = ""

    def action(self, outcome=True):
        """
        :param outcome: Boolean for successful or unsuccessful action
        :return None:
        """
        self._operations += 1
        if outcome:
            self._successful_operations += 1


def recursive_type(obj):
    # This assumes the first item in a list is the same as every item in that list (As it should be)

    this = type(obj)
    result = "["

    if this is list:
        for item in this:
            result += "%s, " % recursive_type(item)
            
        result = result[:-2] + "]"
    else:
        result = (str(type(this))[8:-2])

    return result
