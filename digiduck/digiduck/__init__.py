import sys
from ducklex import splitpass, lexpass
from dparser import parseseq

banner = "// DigiDuck code courtesy of uslurper. https://github.com/uslurper\n// This program currently does not allow the BREAK key, since I couldn't find it in the USB HID spec.\n\n"
begstr = """#include "DigiKeyboard.h"\n\n#define KEY_TAB 43\n#define KEY_DOWN 81\n#define KEY_DELETE 42\n#define KEY_PRINTSCREEN 70\n#define KEY_SCROLLLOCK 71\n#define KEY_INSERT 73\n#define KEY_PAUSE 72\n#define KEY_HOME 74\n#define KEY_PAGEUP 75\n#define KEY_END 77\n#define KEY_PAGEDOWN 78\n#define KEY_RIGHTARROW 79\n#define KEY_RIGHT 79\n#define KEY_DOWNARROW 81\n#define KEY_LEFTARROW 80\n#define KEY_UP 82\n#define KEY_UPARROW 82\n#define KEY_NUMLOCK 83\n#define KEY_CAPSLOCK 57\n#define KEY_MENU 118\n\n"""
setup = """void setup() {\n\n"""
recurring = "\n}\n\nvoid loop() {\n\n"
ending = "\n}"


def usage():
    print("DIGIDUCK: Ducky Script to Digispark compiler")
    print()
    print()
    print("Usage: digiduck [duckyscript.txt]")
    print("       digiduck [duckyscript.txt] [outputfile.ino]")
    print()
    print("Once you have your output, just open in your Arduino IDE. I'm not going to tell you how to set up your Digispark, you can handle it.")


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        file = open(filename)
        characters = file.read()
        file.close()
        tokens = splitpass(lexpass(characters))
        x = parseseq(tokens)
        if len(sys.argv) == 3:
            f = open(sys.argv[2], 'w')
        else:
            name = sys.argv[1].split(".") + ".ino"
            f = open(name, 'w')
        f.write(banner + begstr + "".join(x[0]) + setup + "".join(x[1]) + "".join(x[2]) + recurring + "".join(x[3]) + ending)
        f.close()
        print("Done.")
        sys.exit(0)
    else:
        usage()
