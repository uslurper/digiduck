import lexer
from iterutils import groupby

RESERVED = 'RESERVED'
INT = 'INT'
KEY = 'KEY'
MODKEY = 'MODKEY'
STR = 'STR'
NEWLINE = 'NEWLINE'

strreg = r'[-!$%^&*@()_+|~=`{}\[\]:\";\'<>\\?,./A-Za-z0-9 ][-!$%^@&*()_+|~=`{}\[\]:\";\'<>\\?,./A-Za-z0-9 ]+'

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
    (r'[0-9]+',                       INT),
    (r'STRING',                  RESERVED),
    (strreg,                          STR),
    (r'[A-Za-z][ \t]?',              KEY),
    (r'[-!$%^&*@()_+|~=`{}\[\]:\";\'<>\\?,./]', STR),
]


def lexpass(characters):
    return lexer.lex(characters, token_exprs)


def splitpass(toklist):
    l = toklist
    splitlist = [list(group) for k, group in groupby(l, lambda x: x == ("", "NEWLINE")) if not k]
    return splitlist
