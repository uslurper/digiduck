import sys
import re


def lex(characters, token_exps):
    pos = 0
    tokens = []
    lines = characters.splitlines()
    schar = ""
    for line in lines:
        schar += line.strip() + "\n"
    while pos < len(schar):
        match = None
        for token_expr in token_exps:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(schar, pos)
            if match:
                text = match.group(0).strip()
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal Character: %s\n' % schar[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
