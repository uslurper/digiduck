# digiduck
This program compiles Ducky Script into something usable for the Digispark ATTiny 85 chip. Get yourself a $1 USB Rubber Ducky.

Available on pip: pip install digiduck

There is a great deal of functionality beyond standard Ducky Script planned for the future.

The REPEAT command can either work as usual, or it can be used with two arguments:
REPEAT 4 10 means "repeat the previous four instructions 10 times".
REPEATS can also now be nested.

You can now trigger the light on your digispark within the ducky script via the commands "LIGHT ON" or "LIGHT OFF". This may be useful for feedback during execution.

Additionally, there is now a keyword, RTRIGGER, which allows certain code to be run randomly at specified intervals. RTRIGGER takes one or two arguments, the first being the percentage of successes desired and the second being the time interval between attempts. This time interval is formatted as 10s for 10 seconds, 10m for 10 minutes, 10h and 10d for hours and days, respectively. All RTRIGGER blocks must be terminated with the ENDR keyword, but can be placed anywhere in code. Errors will occur if you place one inside of a repeat block though. If a time duration is not specified, it defaults to one second. Also, the initial frequency parameter is capable of accepting floating point values.

Please note that the program discards leading whitespace between your opening keywords and their arguments in the Ducky Script. This negatively affects ASCII art.
