import subprocess
import time

from components.framework.FwComponentGadget import FwComponentGadget
from components.helpers.Format import Format


class Keyboard(FwComponentGadget):
    """
       Class that handles all Keyboard functionality

           Args:
              enabled:          boolean - enable/disable instant start
              debug:            boolean - enable/disable debug features
              id_vendor         string - vendor id to be used by keyboard
              id_product        string - product id to be used by keyboard

          functions:
              write             write string using emulated keyboard
              run               run a specified ducky script

          Returns:
              Keyboard Object

          Raises:
              IOError on failure to send data to target device
              ValueError on bad delay/string_delay
      """

    def __init__(self, path, keyboard_layout="default.keyboard", language_layout="default.language", enabled=False, debug=False):
        super().__init__(driver_name="g_hid", enabled=enabled, debug=debug, name="keyboard", type="component")

        # Debug params
        self._debug = debug
        self._type = "Component"
        self._name = "Keyboard"

        self.path = path
        self.keyboard_path = path + "/framework/shell_scripts/hid-gadget-test"

        self.debug("Initializing Keyboard...", color=Format.color_primary)

        # TODO add language/layout support
        # stores .keyboard layout
        self.keyboard_layout = keyboard_layout
        # stores .language layout
        self.language_layout = language_layout

        # defaults
        self.default_delay = 1000  # 1000ms / 1s default
        self.__keyboard = ""

        # dummy last commands
        self.command = ""
        self.last_command = ""

        # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt (Like ducky)
        self.__special_char_equivalent = {
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

        self.__key_equivalent = {
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

            # TODO ADD F1-12
        }

        self.__command_equivalent = {
            "CTRL-ALT-DELETE": "left-ctrl left-alt delete",
            "CTRL-SHIFT-ESC": "left-ctrl left-shift escape"

        }

    # Handles string write to target
    def write(self, string=""):
        """
        :param string: what is to be typed with keyboard
        :return None:

        """

        if string:
            for character in string:
                keypress = self.__resolve_ascii(character)
                if keypress:
                    self.__send_data(keypress)

    def resolve_script(self, script, script_name=""):
        """
        :param script:          contents of script
        :param script_name:     name of script
        :return :
        """
        for line in script:
            self.resolve_line(current_line=line)
        self.debug("Script %s resolved" % script_name,  color=Format.color_info)
        return

    def __send_data(self, data):
        """
        NOT FOR INDIV USE

        :param data: what is to be typed with keyboard
        :return boolean: whether send was successful
        """

        self.debug("SENDING DATA: " + data)
        try:
            # Set timeout at 1s as it will otherwise wait for ages expecting more input
            output = subprocess.call("echo "+data+" | " + self.keyboard_path + " /dev/hidg0 keyboard > /dev/null", timeout=1)
            # if "rror" in output:
            #     self.debug("ERROR: "+output)
            #     raise IOError("Failure to send data")

        except Exception as e:
            self.debug("Warning: %s" % e, color=Format.color_warning)
            return False
        return True

    def __resolve_ascii(self, character):
        """
        NOT FOR INDIV USE

        :param character:
        :return resolved character:
        """
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
            resolved_character = self.__special_char_equivalent.get(character, "")

        return resolved_character

    def __resolve_args(self, args):
        """
        NOT FOR INDIV USE

        :param args:
        :return resolved  arguments:
        """
        args = args.split()
        resolved_args = ""
        if len(args) < 6:
            for arg in args:
                # is arg a key?
                arg_resolved = self.__key_equivalent.get(arg, "")
                if not arg_resolved:
                    # is arg ascii character?
                    arg_resolved = self.__resolve_ascii(arg)
                if not arg_resolved:
                    # is arg command?
                    arg_resolved = self.__command_equivalent.get(arg, "")

                # if arg has been resolved, add it to resolved args
                if arg_resolved:
                    resolved_args += (" " + arg_resolved)
            return resolved_args

    def resolve_line(self, current_line):
        """
        :param current_line:
        :return resolved line:
        """
        # If line is blank, skip
        if current_line == '\n':
            return

        # Remove newline characters and split lines into command and arguments
        command, whitespace, args = current_line.strip('\n').partition(" ")

        # Input debugging
        self.debug("command in = " + command)
        self.debug("arg/s in = " + args)

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
                        self.__send_data(keypress)

        elif command == "STRING_DELAY":
            if args:
                delay, _, string = args.partition(' ')

                try:
                    # Attempt to convert delay to int
                    delay = int(delay.strip())
                    delay /= 1000.0
                except ValueError:
                    # Delay was not an int
                    self.debug("Resolve Error: bad delay format", color=Format.color_warning)
                    self.debug("Using default delay( " + str(self.default_delay) + "ms)", color=Format.color_warning)
                    delay = self.default_delay / 1000.0
                else:
                    # Delay was an int
                    self.debug("delay string for " + str(delay))

                for character in string:
                    keypress = self.__resolve_ascii(character)
                    time.sleep(delay)
                    if keypress:
                        self.__send_data(keypress)

        elif command == "DELAY":
            if args:
                delay, _, string = args.partition(' ')

                try:
                    # Attempt to convert delay to int
                    delay = int(delay.strip())
                    delay /= 1000.0
                except ValueError:
                    # Delay was not an int
                    self.debug("Resolve Error: bad delay format", color=Format.color_warning)
                    self.debug("Using default delay( " + str(self.default_delay) + "ms)", color=Format.color_warning)
                    delay = self.default_delay / 1000.0
                else:
                    # Delay was an int
                    self.debug("delay for " + str(delay))
                time.sleep(delay)

        elif command in self.__key_equivalent:
            resolved_command = self.__key_equivalent.get(command, '')
            if not args:
                self.__send_data(resolved_command)
            else:
                self.__send_data(resolved_command + self.__resolve_args(args))

        # Resolve multi-part commands
        # ---------------------------
        elif command.count("-") == 1:  # TODO - Implement similar interpreter for multi - commands
            command_1, unused, command_2 = command.partition("-")
            self.__send_data(
                self.__key_equivalent.get(command_1, '') + " " + self.__key_equivalent.get(command_2, '') + self.__resolve_args(args))

        elif command == "MENU":
            if not args:
                return ""
            else:
                self.__send_data(
                    self.__key_equivalent.get("GUI", '') + " " + self.__key_equivalent.get("ALT", '') + self.__resolve_args(args))

        elif command == "REPEAT":
            # Repeat last command
            # Done this "weird" way so that delays etc still work
            self.resolve_line(self.last_command)

            # Done in a "weird" way so that delays etc still work
        self.last_command = current_line

    def __del__(self):
        super().disable()  # Disable keyboard driver
