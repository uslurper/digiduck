import lexer
from iterutils import groupby

#Here we set up some keywords. Honestly, this is only written like this because constantly wrapping things in quotes is the road to madness.
RESERVED = 'RESERVED'
INT = 'INT'
KEY = 'KEY'
MODKEY = 'MODKEY'
STR = 'STR'
NEWLINE = 'NEWLINE'
TIME = 'TIME'
FLOAT = 'FLOAT'

#This is just a regex designed to capture any kind of string. It's useful and the worst thing in the world to write down, so it's a variable now.
strreg = r'[-!$%^&*@()_+|~=`{}\[\]:\";\'<>\\?,./A-Za-z0-9 ][-!$%^@&*()_+|~=`{}\[\]:\";\'<>\\?,./A-Za-z0-9 ]+'

#Here's our regices to match to form our token list, regex on the left, designated type on the right.
#The order here matters a lot. We have to make sure more specific patterns are matched before more general ones.
token_exprs = [
    (r'[ \t]+',                      None),
    (r'\n',                       NEWLINE),
    (r'REM',                     RESERVED),
    (r'LIGHT',                   RESERVED),
    (r'ON',                      RESERVED),
    (r'OFF',                     RESERVED),
    (r'DEFAULT_DELAY',           RESERVED),
    (r'DEFAULTDELAY',            RESERVED),
    (r'DELAY',                   RESERVED),
    (r'STRING',                  RESERVED),
    (r'ENDR',                    RESERVED),
    (r'GUI',                       MODKEY),
    (r'WINDOWS',                   MODKEY),
    (r'APP',                          KEY),
    (r'MENU',                         KEY),
    (r'SHIFT',                     MODKEY),
    (r"INSERT",                       KEY),
    (r'DELETE',                       KEY),
    (r'HOME',                         KEY),
    (r'PAGEUP',                       KEY),
    (r'PAGEDOWN',                     KEY),
    (r'UPARROW',                      KEY),
    (r'DOWNARROW',                    KEY),
    (r'LEFTARROW',                    KEY),
    (r'RIGHTARROW',                   KEY),
    (r'TAB',                          KEY),
    (r'ALT',                       MODKEY),
    (r'END',                          KEY),
    (r'ESC',                          KEY),
    (r'ESCAPE',                       KEY),
    (r'F[0-9]+',                      KEY),
    (r'SPACE',                        KEY),
    (r'ENTER',                        KEY),
    (r'CONTROL',                   MODKEY),
    (r'CTRL',                      MODKEY),
    (r'BREAK',                        KEY),
    (r'PAUSE',                        KEY),
    (r'DOWN',                         KEY),
    (r'LEFT',                         KEY),
    (r'RIGHT',                        KEY),
    (r'UP',                           KEY),
    (r'CAPSLOCK',                     KEY),
    (r'NUMLOCK',                      KEY),
    (r'PRINTSCREEN',                  KEY),
    (r'SCROLLLOCK',                   KEY),
    (r'REPLAY',                  RESERVED),
    (r'REPEAT',                  RESERVED),
    (r'RTRIGGER',                RESERVED),
    (r'[0-9]+[s|m|h|d]',             TIME),
    (r'[0-9]+',                       INT),
    (r'[0-9]*\.[0-9]+',             FLOAT),
    (r'STRING',                  RESERVED),
    (strreg,                          STR),
    (r'[A-Za-z][ \t]?',              KEY),
    (r'[-!$%^&*@()_+|~=`{}\[\]:\";\'<>\\?,./]', STR),
]

#I just put the actual lexer code into a separate file for organization purposes. This looks nicer.
def lexpass(characters):
    return lexer.lex(characters, token_exprs)

#This splits the token list into a list of lists containing the tokens found on each individual line.
#This is pretty dense and I don't recommend touching it.
def splitpass(toklist):
    l = toklist
    splitlist = [list(group) for k, group in groupby(l, lambda x: x == ("", "NEWLINE")) if not k]
    return splitlist
