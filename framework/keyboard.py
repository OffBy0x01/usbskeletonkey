import FwComponent
# -*- coding: utf-8 -*-


class Keyboard(FwComponent):
    # still to add: return, enter, esc, escape, backspace, meta, ctrl, shift, alt
    char_eqv = {
        " ": "space",
        "   ": "tab",
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
        "{":" left-shift lbracket",
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
