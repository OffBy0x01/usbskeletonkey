import subprocess

from framework import FwComponentGadget


# -*- coding: utf-8 -*-


class Keyboard(FwComponentGadget):
    def __init__(self, enabled=False, other=False, debug=False):
        # to set the things of the parent class
        super().__init__(driver_name="g_hid", enabled=False, debug=False)
        self.other = other  # doesn't do shit just for demo
        self.debug = debug

    # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt, tab
    char_eqv = {
        " ": "space",
        # "   ": "tab", ## This isn't actually a Tab, its the IDE's interpretation
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
            # something went horribly wrong or I've missed a character
            subprocess.call("%s | %s/hid-gadget /dev/hidg0 keyboard > /dev/null" % (current_char, dir_path), shell=True)
