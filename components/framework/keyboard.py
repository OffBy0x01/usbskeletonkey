import os
import subprocess
import time

from components.framework.FwComponentGadget import FwComponentGadget


class Keyboard(FwComponentGadget):
    def __init__(self, keyboard_layout="default.keyboard", language_layout="default.language", enabled=False,
                 debug=False):
        # to set the things of the parent class
        self._type = "Component"
        self._name = "Keyboard"
        # super().__init__(driver_name="g_hid", enabled=enabled, debug=debug, name="keyboard", type="component")

        # TODO add language/layout support
        # stores .keyboard layout
        self.keyboard_layout = keyboard_layout
        # stores .language layout
        self.language_layout = language_layout

        # defaults
        self._delay = 1  # 1s default
        self._debug = True

        self.__keyboard = "/dev/hidg0 keyboard"

        # dummy last commands
        self.command = []
        self.last_command = ""



        # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt (Like ducky)
        self.special_char_equivalent = {
            " ": "space",
            "	": "tab",  # For the rare occasion
            "`": "backquote",
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
            "[": "lbracket",
            "]": "rbracket",
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
            "?": "left-shift slash",
            "\n": ""  # We don't like your kind around here
        }

        # TODO #1.1 write the default case for this
        self.key_equivalent = {
            # Standard Commands
            "GUI": "left-meta",
            "WINDOWS": "left-meta",
            "MENU": "menu",
            "APP": "menu",
            "SHIFT": "left-shift",
            "ALT": "left-alt",
            "CONTROL": "left-ctrl",
            "CTRL": "left-ctrl",

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
            "PRINTSCREEN": "print",
            "SCROLLLOCK": "scroll-lock",
            "ENTER": "enter",
            "SPACE": "space",
            "TAB": "tab",

        }

    # Handles string write to target
    def write(self, string):
        curr_char = ''

        for c in string:
            if c.isalpha() and c.isupper():
                curr_char = "left-shift %s" % (c.lower())
            elif c.isalpha or c.isdigit:
                curent_char = c
            else:
                # special characters need string equivalents
                curr_char = self.special_char_equivalent.get(c, 0)
                if curr_char is None:
                    super().debug("curr_char is None")

            subprocess.call("%s | %s/hid-gadget /dev/hidg0 keyboard > /dev/null" % (curr_char, "DEFAULT_PATH"),
                            shell=True)

    def __resolve_key(self, key):
        key_eqv = self.key_equivalent.get(key, '')
        self.debug(key + " -> resolve key -> " + key_eqv)
        return key_eqv

    def __resolve_ascii(self, character):
        start_c = character
        if start_c.isalpha() and start_c.isupper():
            character = "left-shift %s" % (start_c.lower())
        elif start_c.isalpha() or start_c.isdigit():
            pass  # Character should remain the same
        else:
            # special characters need string equivalents
            character = self.special_char_equivalent.get(start_c, '')
        if start_c is None:
            self.debug("curr_char is None")
        self.debug(start_c + " -> resolve ASCII -> " + character)
        return character

    # Returns the ducky command on this line
    def __resolve_line(self, current_line):
        """Converts line of file to usable form"""
        output = []

        command, _, args = current_line.partition(" ")  # Split line at first whitespace into cmd and args

        command = command.strip('\n')
        args = args.strip('\n')

        self.debug("COMMAND IN = " + command)
        self.debug("ARGS IN = " + args)

        if command == "REM":
            # Comment, so do nothing
            return ""

        elif command == "STRING":
            if not args:
                return ""
            else:
                for character in args:
                    keypress = self.__resolve_ascii(character=character)
                    if keypress:
                        output.append(keypress)

        elif command == "STRING_DELAY":
            if not args:
                return ""
            else:
                delay, string = args.split(maxsplit=1)

                # Ensure additional characters have been removed
                delay = int(delay.strip())
                try:
                    # Hopefully it doesn't matter where the delay is
                    time.sleep(delay / 1000.0)
                except ...:
                    self.debug("could not DELAY for" + str(delay) + "ms.")
                    self.debug("Skipping DELAY of " + command)

                for character in args:
                    keypress = self.__resolve_ascii(character=character)
                    if keypress:
                        output.append(keypress)



        elif command == "DELAY":
            delay = int(args.strip())
            try:
                delay = delay / 1000.0
            except ...:
                self.debug("could not DELAY for" + str(delay) + "ms.")
                self.debug("Skipping DELAY of " + command)
            else:
                self.debug("DELAY for " + str(delay) + "ms.")
                time.sleep(delay)

        elif command in ("CTRL", "CONTROL"):
            if not args:
                # No args
                output.append(self.__resolve_key("CTRL"))
            else:
                # args or other commands
                output.append(self.__resolve_key("CTRL"))
                output.append(self.__resolve_line(args))

        elif command == "ALT":
            if not args:
                # No args
                output.append(self.__resolve_key("ALT"))
            else:
                # args or other commands
                output.append(self.__resolve_key("ALT"))
                output.append(self.__resolve_line(args))

        elif command == "SHIFT":
            if not args:
                # No args
                output.append(self.__resolve_key("SHIFT"))
            else:
                # args or other commands
                output.append(self.__resolve_key("SHIFT"))
                output.append(self.__resolve_line(args))

        # Resolve multi-part commands
        # ---------------------------
        elif command == "CTRL-ALT":
            if not args:
                return ""
            else:
                output.append(self.__resolve_key("CTRL"))
                output.append(self.__resolve_key("ALT"))
                output.append(self.__resolve_line(args))

        elif command == "CTRL-SHIFT":
            if not args:
                return ""
            else:
                output.append(self.__resolve_key("CTRL"))
                output.append(self.__resolve_key("SHIFT"))
                output += (self.__resolve_line(args))

        elif command == "MENU":
            if not args:
                return ""
            else:
                output.append(self.__resolve_key("GUI"))
                output.append(self.__resolve_key("ALT"))
                output += (self.__resolve_line(args))

        elif command == "ALT-SHIFT":
            if not args:
                return ""
            else:
                output.append(self.__resolve_key("ALT"))
                output.append(self.__resolve_key("SHIFT"))
                output += (self.__resolve_line(args))

        elif command == "ALT-TAB":
            if not args:
                output.append(self.__resolve_key("ALT"))
                output.append(self.__resolve_key("TAB"))
            else:
                # There shouldn't be any args with this
                self.debug("Ignored argument/s \"" + args + "\" in command: " + command)
                return ""

        elif command in ("GUI", "WINDOWS"):
            if not args:
                output.append(self.__resolve_key("GUI"))
            else:
                output.append(self.__resolve_key("GUI"))
                output += (self.__resolve_line(args))

        elif command == "REPEAT":
            # Repeat last command
            # Done this "weird" way so that delays etc still work
            output.append(self.__resolve_line(self.last_command))

        # or handle as raw ascii?
        elif len(command) <= 1 and command.isalnum():
            self.debug("Resolve ASCII for " + command)
            output.append(self.__resolve_ascii(character=command))

        # Otherwise resolve key
        else:
            self.debug("Resolve key for " + command)
            output.append(self.__resolve_key(key=command))

        if output:
            # TODO TO FIX MAJOR ERROR - Tiredness currently limiting ability too much
            """
            Currently fails because sometimes output contains a list of a list,
            fix this by checking the type and converting if it is the wrong type
            something like:
            
            if output == list
               output = ''.join(output)
               
            // But obviously better than that
            
            """
            self.debug("output = " + ' '.join(output))
        else:
            self.debug("No Command Output")

        # Done in a "weird" way so that delays etc still work
        self.last_command = current_line

        return output

    def resolve(self, script):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/../scripts/" + script, "r") as file:
            for line in file:
                print("Resolved line:", ' '.join(self.__resolve_line(current_line=line)), "\n")
