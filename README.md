# digiduck
This program compiles Ducky Script into something usable for the Digispark ATTiny 85 chip. Get yourself a $1 USB Rubber Ducky.

Available on pip: pip install digiduck

There is a great deal of functionality beyond standard Ducky Script planned for the future. 

The REPEAT command can either work as usual, or it can be used with two arguments:
REPEAT 4 10 means "repeat the previous four instructions 10 times".
REPEATS can also now be nested.

Please note that the program discards leading whitespace between your opening keywords and their arguments in the Ducky Script. This negatively affects ASCII art.
