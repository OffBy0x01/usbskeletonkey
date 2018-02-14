import os
import subprocess
import time

from components.framework.FwComponentGadget import FwComponentGadget


class Keyboard(FwComponentGadget):
    def __init__(self, keyboard_layout="default.keyboard", language_layout="default.language", enabled=False,
                 debug=False):

        # Debug params
        self._debug = debug
        self._type = "Component"
        self._name = "Keyboard"

        # set usb gadget properties only when not in debug
        if not self._debug:
            super().__init__(driver_name="g_hid", enabled=enabled, debug=debug, name="keyboard", type="component")

        # TODO add language/layout support
        # stores .keyboard layout
        self.keyboard_layout = keyboard_layout
        # stores .language layout
        self.language_layout = language_layout

        # defaults
        self.default_delay = 1000  # 1000ms / 1s default
        self.__keyboard = "/dev/hidg0 keyboard"

        # dummy last commands
        self.command = ""
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

        self.command_equivalent = {
            "CTRL-ALT-DELETE": "left-ctrl left-alt delete",
            "CTRL-SHIFT-ESC": "left-ctrl left-shift escape"

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

    def send_data(self, data):
        self.debug("SENDING DATA: " + data)
        # TODO ADD G_HID CONTROL HERE

    def __resolve_ascii(self, character):
        resolved_character = ""
        # If character is uppercase letter
        if character.isalpha() and character.isupper():
            resolved_character = "left-shift %s" % (character.lower())
        # If character is a-z or 0-9
        elif character.isalnum():
            # Character should remain the same
            resolved_character = character
        else:
            # Characters must be special character
            resolved_character = self.special_char_equivalent.get(character, "")

        return resolved_character

    def __resolve_args(self, args):
        args = args.split()
        resolved_args = ""
        if len(args) < 6:
            for arg in args:
                # is arg a key?
                arg_resolved = self.key_equivalent.get(arg, "")
                if not arg_resolved:
                    # is arg ascii character?
                    arg_resolved = self.__resolve_ascii(arg)
                if not arg_resolved:
                    # is arg command?
                    arg_resolved = self.command_equivalent.get(arg, "")

                # if arg has been resolved, add it to resolved args
                if arg_resolved:
                    resolved_args += (" " + arg_resolved)
            return resolved_args

    def resolve_line(self, current_line):

        # If line is blank, skip
        if current_line == '\n':
            return

        # Remove newline characters and split lines into command and arguments
        command, whitespace, args = current_line.strip('\n').partition(" ")

        # Input debugging
        self.debug("COMMAND IN = " + command)
        self.debug("ARG/S IN = " + args)

        # Resolve current line:
        # ------------------
        if command == "REM":
            # Comment, so do nothing
            pass

        elif command == "STRING":
            if args:
                for character in args:
                    keypress = self.__resolve_ascii(character)
                    if keypress:
                        self.send_data(keypress)

        elif command == "STRING_DELAY":
            if args:
                delay, _, string = args.partition(' ')

                try:
                    # Attempt to convert delay to int
                    delay = int(delay.strip())
                    delay /= 1000.0
                except ValueError:
                    # Delay was not an int
                    self.debug("BAD DELAY FORMAT")
                    self.debug("USING DEFAULT DELAY ( " + str(self.default_delay) + "ms)")
                    delay = self.default_delay / 1000.0
                else:
                    # Delay was an int
                    self.debug("DELAY_STRING FOR " + str(delay))

                for character in string:
                    keypress = self.__resolve_ascii(character)
                    time.sleep(delay)
                    if keypress:
                        self.send_data(keypress)

        elif command == "DELAY":
            if args:
                delay, _, string = args.partition(' ')

                try:
                    # Attempt to convert delay to int
                    delay = int(delay.strip())
                    delay /= 1000.0
                except ValueError:
                    # Delay was not an int
                    self.debug("BAD DELAY FORMAT")
                    self.debug("USING DEFAULT DELAY ( " + str(self.default_delay) + "ms)")
                    delay = self.default_delay / 1000.0
                else:
                    # Delay was an int
                    self.debug("DELAY_STRING FOR " + str(delay))
                time.sleep(delay)

        elif command in self.key_equivalent:
            resolved_command = self.key_equivalent.get(command, '')
            if not args:
                self.send_data(resolved_command)
            else:
                self.send_data(resolved_command + self.__resolve_args(args))

        # Resolve multi-part commands
        # ---------------------------
        elif command.count("-") == 1:  # TODO - Implement similar interpreter for multi - commands
            command_1, unused, command_2 = command.partition("-")
            self.send_data(
                self.key_equivalent.get(command_1, '') + " " + self.key_equivalent.get(command_2,
                                                                                       '') + self.__resolve_args(args))

        elif command == "MENU":
            if not args:
                return ""
            else:
                self.send_data(
                    self.key_equivalent.get("GUI", '') + " " + self.key_equivalent.get("ALT", '') + self.__resolve_args(
                        args))

        elif command == "REPEAT":
            # Repeat last command
            # Done this "weird" way so that delays etc still work
            self.resolve_line(self.last_command)

            # Done in a "weird" way so that delays etc still work
        self.last_command = current_line

    def resolve(self, script):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/../scripts/" + script, "r") as file:
            for line in file:
                self.resolve_line(current_line=line)
            self.debug("DONE")
