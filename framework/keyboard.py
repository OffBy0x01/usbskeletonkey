import subprocess

from framework.FwComponentGadget import FwComponentGadget


class Keyboard(FwComponentGadget):
    def __init__(self, enabled=False, other=False, debug=False):
        # to set the things of the parent class
        # super().__init__(driver_name="g_hid", enabled=enabled, debug=debug)
        self.other = other  # doesn't do shit just for demo

    # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt (Like ducky)
    char_eqv = {
        " ": "space",
        "	": "tab",  # Took from notepad should work
        "!": "left-shift 1",
        "\"": "left-shift 2",
        "£": "left-shift  3",
        "$": "left-shift 4",
        "%": "left-shift 5",
        "^": "left-shift 6",
        "&": "left-shift 7",
        "*": "left-shift 8",
        "(": "left-shift 9",
        ")": "left-shift 0",
        "-": "minus",
        "_": "left-shift minus",
        "=": "equals",
        "+": "left-shift equals",
        "{": " left-shift lbracket",
        "}": "left-shift rbracket",
        ";": "semi-colon",
        ":": "left-shift semi-colon",
        "'": "quote",
        "@": "left-shift quote",
        "#": "hash",
        "~": "left-shift hash",
        "\\": "backslash",
        "|": "left-shift backslash",
        ",": "comma",
        "<": "left-shift comma",
        ".": "period",
        ">": "left-shift period",
        "/": "slash",
        "?": "left-shift slash"
    }

    # Handles string write to target
    def write_to_target(self, string):
        current_char = ''

        for c in string:
            if c.isalpha() and c.isupper():
                current_char = "left-shift %s" % (c.lower())
            elif c.isalpha or c.isdigit:
                curent_char = c
            else:
                # special characters need string equivalents
                current_char = self.char_eqv.get(c, 0)
                if current_char is None:
                    super().debug("something went horribly wrong or I've missed a character")

            subprocess.call("%s | %s/hid-gadget /dev/hidg0 keyboard > /dev/null" % (current_char, "DEFAULT_PATH"),
                            shell=True)  # Documentation says use .run() unless Py < 3.5 - is this intentional?

    # Might not need this but just theorizing
    def get_script(self, path):
        print(0)

    def exec(self, script):
        file = open(script, "r")
        for line in file:
            print(line, end="")
        # Needs:
        #   read scripts line by line
        #   interpret command and args sep
        #   have a queue of scripts to run?
        #       remove method for once each item has completed
        #       repeat item if needed to run multiple times
        #
        #   clean-up method
        #   use enable and disable as per FwComponentGadget


# debugging
if __name__ == '__main__':
    test = Keyboard()
    test.exec("test.txt")
