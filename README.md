# daisy font converter

A small command line tool to convert [PixelForge](https://www.pixel-forge.com/) font files into c-arrays for the electrosmith daisy.

## Usage

```bash
daisyfontconverter --input pat/to/my_font.pxf --width 4 --height g
```

### Example output

```c
static const uint16_t Font4x6[] = {
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, // Space
    0x0000, 0x4000, 0x4000, 0x4000, 0x0000, 0x4000, // !
    0x0000, 0xA000, 0xA000, 0x0000, 0x0000, 0x0000, // "
    ...
    0x0000, 0x0000, 0xE000, 0x2000, 0x4000, 0xE000, // z
    0x0000, 0x6000, 0x4000, 0xC000, 0x4000, 0x6000, // {
    0x0000, 0x4000, 0x4000, 0x4000, 0x4000, 0x4000, // |
    0x0000, 0xC000, 0x4000, 0x6000, 0x4000, 0xC000, // }
    0x0000, 0x0000, 0x2000, 0xE000, 0x8000, 0x0000, // ~ Tilde
};

FontDef Font_4x6 = {4, 6, Font4x6};
```

The result of that output should go into `oled_fonts.c` in libDaisy.
Additionally put a `extern FontDef Font_4x6;` into `oled_fonts.h`

Run `task build_all` in VSCode and use your font as usually

### Installation

**Option A:** just download the python script in the daisyfontconverter directory (no external dependencies) and run it with python:

```bash
python3 cli.py -input pat/to/my_font.pxf --width 4 --height g
```

**Option B:** Install via pip using

```bash
pip install daisyfontconverter
```

and run via
```bash
daisyfontconverter --input pat/to/my_font.pxf --width 4 --height g
```