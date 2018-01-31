import subprocess

from framework.FwComponentGadget import FwComponentGadget


class Keyboard(FwComponentGadget):
    def __init__(self, enabled=False, other=False, debug=False):
        # to set the things of the parent class
        super().__init__(driver_name="g_hid", enabled=enabled, debug=debug)
        self.other = other  # doesn't do shit just for demo

        # defaults
        self._delay = 1  # 1s default
        self.command = self.ignore
        self.last_command = self.command

        # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt (Like ducky)
        self.char_eqv = {
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

        # TODO #1.1 write the default case for this
        self.commands = {
            # TODO # 0 Recursively build commands to support multi-special-key-based commands
            "REM": self.ignore,
            "DEFAULTDELAY": self.set_delay,
            "DEFAULT_DELAY": self.set_delay,  # Same as DEFAULTDELAY
            "DELAY": self.delay,
            "STRING": self.write,
            "GUI": self.super_key,
            "WINDOWS": self.super_key,
            "MENU": "menu",  # TODO #ATSOMEPOINT Work out how the fuck to do this
            "APP": "menu",  # As above
            "SHIFT": self.mod_key,
            "ALT": self.mod_key,
            "CONTROL": self.mod_key,
            "CTRL": self.mod_key,
            # TODO #2 look at arrow keys and 'Extended Commands'
            # Arrow Keys
            "DOWNARROW": "down",
            "DOWN": "down",
            "LEFTARROW": "left",
            "LEFT": "left",
            "RIGHTARROW": "right",
            "RIGHT": "right",
            "UPARROW": "up",
            "UP": "up",
            # Extended Commands
            "BREAK": "pause",
            "PAUSE": "pause",
            "CAPSLOCK": "caps-lock",
            "DELETE": "delete",
            "ESC": "escape",
            "ESCAPE": "escape",
            "HOME": "home",
            "INSERT": "insert",
            "NUMLOCK": "num-lock",
            "PAGEUP": "pageup",
            "PAGEDOWN": "pagedown",
            "PRINTSCREEN": "",  # No idea
            "SCROLLLOCK": "scroll-lock",
            "SPACE": "space",
            "TAB": "tab",

            "REPEAT": self.repeat_command
        }

    # TODO #3 improve comments
    # Handles string write to target
    def write(self, string):
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

    def ignore(self):
        pass

    def set_delay(self, delay=1):
        self._delay = delay

    def delay(self, delay=-1):
        if delay == -1:
        # use self._delay
        else:

    # use delay

    def super_key(self):
        pass

    def mod_key(self):
        if self.command == "SHIFT":
        # do shift
        elif self.command == "ALT":
        # do alt
        elif self.command == "CONTROL" or self.command == "CTRL":
        # do control
        else:
            pass  # Shouldn't be here

    def repeat_command(self):
        self.last_command()

        #TODO fix this

    # Might not need this but just theorizing
    def get_script(self, path):
        print(0)

    # TODO #1 finish command interpreter
    def exec(self, script):
        file = open(script, "r")
        for line in file:
            print(line, end="")
            # split into command and value
            command_value = line.split(maxsplit=1)
            try:
                self.command = self.commands.get(command_value[0])
                self.debug("Looking for command in commands")

            except KeyError:  # command not found
                self.debug("Error: could not find command in commands")

            else:  # command was found
        # TODO If command not single input then check for other commands
        # TODO If command was single input then do the functions




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
