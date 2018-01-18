import FwComponent
# -*- coding: utf-8 -*-


class Keyboard(FwComponent):
    def __init__(self, enable=False, other):

        # to set the things of the parent class

        super().__init__(driver_name="g_hid", enable=False)

        self.other = other  # doesn't do shit just for demo

    # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt, tab
    char_eqv = {
        " ": "space",
        # "   ": "tab", ## This isnt actually a Tab, its the IDE's interpretation
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

    def write(string):

        for c in string:

            if c.isalpha() & & c.isupper():

                current_char = "left-shift %s" % (c.lower())

            elif c.isalpha or c.isdigit:

                curent_char = c

            else:

                # special characters need string equivalents

                current_char = char_eqv[input()]()

                if current_char is None:

            # something went horribly wrong or I've missed a character

            subprocess.call("%s | %s/hid-gadget /dev/hidg0 keyboard > /dev/null" % (current_char, dir_path), shell=True)
