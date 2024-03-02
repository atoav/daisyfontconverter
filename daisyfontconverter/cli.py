#!/usr/bin/python

import os
import re
import sys
import argparse




ascii_names = {
    32: "Space",
    33: "!",
    34: "\"",
    35: "#",
    36: "$",
    37: "%",
    38: "&",
    39: "'",
    40: "(",
    41: ")",
    42: "*",
    43: "+",
    44: ",",
    45: "-",
    46: ".",
    47: "/",
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
    58: ":",
    59: ";",
    60: "<",
    61: "=",
    62: ">",
    63: "?",
    64: "@",
    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
    71: "G",
    72: "H",
    73: "I",
    74: "J",
    75: "K",
    76: "L",
    77: "M",
    78: "N",
    79: "O",
    80: "P",
    81: "Q",
    82: "R",
    83: "S",
    84: "T",
    85: "U",
    86: "V",
    87: "W",
    88: "X",
    89: "Y",
    90: "Z",
    91: "[",
    92: "backslash",
    93: "]",
    94: "^",
    95: "_ underscore",
    96: "` backtick",
    97: "a",
    98: "b",
    99: "c",
    100: "d",
    101: "e",
    102: "f",
    103: "g",
    104: "h",
    105: "i",
    106: "j",
    107: "k",
    108: "l",
    109: "m",
    110: "n",
    111: "o",
    112: "p",
    113: "q",
    114: "r",
    115: "s",
    116: "t",
    117: "u",
    118: "v",
    119: "w",
    120: "x",
    121: "y",
    122: "z",
    123: "{",
    124: "|",
    125: "}",
    126: "~ Tilde",
}


def main():
    parser = argparse.ArgumentParser(
                        prog='daisy font converter',
                        description='Converts PixelForge .pxf files into a suitable .c file for libdaisy oled displays',
                        epilog='author: atoav')

    parser.add_argument('-i', '--input', type=argparse.FileType('r'), required=True, help="PixelForge .pxf file to convert")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help="path for output (printed to stdout otherwise)")
    parser.add_argument('--width', type=int, required=True, help="Width of the Font (including space between characters)")
    parser.add_argument('--height', type=int, required=True, help="Height of the Font (including space between lines)")
    parser.add_argument('--name', help="Optional name (only use characters permitted in a C++ variable name)")

    args = parser.parse_args()
    if args.name is not None:
        args.name = args.name.replace(" ", "_").replace("*", "_")

    glyphs = {}

    with args.input as f:
        lines = f.readlines()
        glyph = None
        for line in lines:
            if line.startswith("format_version:"):
                version = line.split(": ")[1].strip()
                if version != "1.0":
                    print(f"Warning: This is a PixelForge Font file with version {version}, this script was made for version 1.0, check your output! ")
            if match := re.match(r'^\t(\d*):', line):
                glyph = int(match.group(1))
            elif match := re.match(r'^\t*pixels: (\d* \d*,\s)*', line):
                values = line.split(": ")[1].split(",")
                values = [v.strip() for v in values]
                values = [(int(v.split(" ")[0]), int(v.split(" ")[1])) for v in values if v.strip() != ""]
                glyphs[glyph] = values


    # Pixelforge does not create space characters, so lets do it ourselves
    space = '0x0000, ' * args.height
    space += f'// {ascii_names[32]}'
    output = {
        32: space
    }

    # Generate the C++ variables
    for glyph, values in glyphs.items():
        output[glyph] = ""
        for y in range(args.height):
            y = args.height - 1 - y
            x_values = [v[0] for v in values if v[1] == y]
            bin_str = ""
            # We are using uint16_t so use 16 bits..
            for x in range(16):
                if x in x_values:
                    bin_str += "1"
                else:
                    bin_str += "0"
            val = int(bin_str, 2)
            hex_val = f'{val:04x}'
            output[glyph] += f'0x{str(hex_val).upper()}, '
        output[glyph] += f'// {ascii_names[glyph]}'

    name = 'Font' if args.name is None else f'Font{args.name}'

    out_str = f"static const uint16_t {name}{args.width}x{args.height}[] = {{\n"

    for _glyph, text in output.items():
        out_str += f'    {text}\n'
    out_str += '};\n\n'

    out_str += f'FontDef {name}_{args.width}x{args.height} = {{{args.width}, {args.height}, {name}{args.width}x{args.height}}};\n\n'

    if args.output is None:
        print(out_str)
        print("// Add this to oled_fonts.h:")
        print(f"// extern FontDef {name}_{args.width}x{args.height}")
    else:
        with args.output as f:
            f.write(out_str)
        print(f"Written output\n")
        print("Don't forget to add this to oled_fonts.h:")
        print(f"extern FontDef {name}_{args.width}x{args.height}")
                
if __name__ == "__main__":
    main()