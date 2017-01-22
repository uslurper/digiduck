**DigiDuck: Ducky Script to Digispark**
=======================================
This is a simple program that converts Ducky Script for Hak5 USB Rubber Duckys into code executable by a Digispark.
As of yet there is no support for the BREAK key, but all other keys work fine.

The REPEAT command can either work as usual, or it can be used with two arguments:
REPEAT 4 10 means "repeat the previous four instructions 10 times".
REPEATS can also now be nested.

Please note that the program discards leading whitespace between your opening keywords and their arguments in the Ducky Script. This negatively affects ASCII art.

Written by `Uslurper <https://github.com/uslurper>`_.

Usage: digiduck [source.txt] [dest.txt]

It's that simple.
