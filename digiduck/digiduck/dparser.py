import sys

# Let's define some useful strings

digistr = "DigiKeyboard."


def escstr(string):
    newstr = string.replace('\\', '\\\\').replace('"', r'\"').replace('%', r'%%')
    return newstr


def autoindent(strlist):
    result = []
    for line in strlist:
        result.append("\t" + line)
    return result


def digidelay(integer):
    if integer == 0:
        return []
    return ["\t" + digistr + ("delay(%d)" % integer) + ";\n", "\tDigiKeyboard.sendKeyStroke(0);\n"]


def digiprint(string, defdel):
    r = ["\t" + digistr + ("println(\"%s\")" % escstr(string)) + ";\n"]
    r.extend(digidelay(defdel))
    return r


def keypress(keys, defdel):
    r = ["\t" + digistr + ("sendKeyStroke(%s)" % keys) + ";\n"]
    r.extend(digidelay(defdel))
    return r


def repeat(prev, integer, lev):
    p = []
    for l in prev:
        if l != [""]:
            p.extend(l)
    body = ["\tfor (i%d=0; i%d<%d; i%d++) {\n" % (lev, lev, integer, lev)]
    body.extend(autoindent(p))
    body.append("\t}\n")
    return body


def modconvert(string):
    if string in ("GUI", "WINDOWS"):
        return "MOD_GUI_LEFT"
    elif string in ("CONTROL", "CTRL"):
        return "MOD_CTRL_LEFT"
    elif string == "ALT":
        return "MOD_ALT_LEFT"
    elif string == "SHIFT":
        return "MOD_SHIFT_LEFT"


def parseseq(seq):
    endstr = []
    decs = set()
    lev = 0
    for i in range(len(seq)):
        if i == 0:
            defdel = 0
        pos = 0
        tdel = defdel
        if i + 1 == len(seq):
            defdel = 0
        while pos < len(seq[i]):
            if seq[i][pos][1] == 'RESERVED':
                if seq[i][pos][0] == "REM":
                    for t in range(1, len(seq[i])):
                        com = ""
                        com += seq[i][pos + t][0]
                    endstr.append(["\t// " + com + "\n"])
                    break
                elif seq[i][pos][0] in ("DEFAULT_DELAY", "DEFAULTDELAY"):
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        defdel = int(seq[i][pos][0])
                        break
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: DEFAULTDELAY takes an integer argument." % i)
                        break
                elif seq[i][pos][0] == "DELAY":
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        endstr.append(digidelay(int(seq[i][pos][0])))
                        break
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: DELAY takes an integer argument." % i)
                        break
                elif seq[i][pos][0] == "STRING":
                    pos += 1
                    if seq[i][pos][1] == "STR":
                        endstr.append(digiprint(seq[i][pos][0], defdel))
                        pos += 1
                        break
                    elif seq[i][pos][1] == "KEY":
                        endstr.append(keypress(seq[i][pos][0].upper(), defdel))
                        break
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: STRING takes a string argument." % i)
                        break
                elif seq[i][pos][0] in ("REPEAT", "REPLAY"):
                    pos += 1
                    repcount = 0
                    prev = []
                    lcount = 1
                    if len(seq[i]) == 2:
                        if seq[i][pos][1] == "INT":
                            repcount = int(seq[i][pos][0])
                        else:
                            sys.stderr.write(
                                "Illegal Op on line %d: REPEAT takes integer args." % i)
                        prev.append(endstr[i - 1])
                    elif len(seq[i]) == 3:
                        if seq[i][pos][1] == "INT":
                            lcount = int(seq[i][pos][0])
                            pos += 1
                            if seq[i][pos][1] == "INT":
                                repcount = int(seq[i][pos][0])
                            else:
                                sys.stderr.write(
                                    "Illegal Op on line %d: REPEAT takes integer args." % i)
                            for j in range(lcount, 0, -1):
                                prev.append(endstr[i - j])
                        else:
                            sys.stderr.write(
                                "Illegal Op on line %d: REPEAT takes integer args." % i)
                    else:
                        sys.stderr.write("Illegal Syntax on line %d: REPEAT takes 1-2 args.")
                    tls = repeat(prev, repcount, lev)
                    lev += 1
                    for j in range(lcount):
                        endstr.pop()
                    for j in range(lcount):
                        endstr.append([""])
                    endstr.append(tls)
                    break
                elif seq[i][pos][0] == "LIGHT":
                    pos += 1
                    decs.add("\tpinMode(0, OUTPUT);\n")
                    decs.add("\tpinMode(1, OUTPUT);\n")
                    if seq[i][pos][0] == "ON":
                        endstr.append(["\tdigitalWrite(0, HIGH);\n", "\tdigitalWrite(1, HIGH);\n"])
                    elif seq[i][pos][0] == "OFF":
                        endstr.append(["\tdigitalWrite(0, LOW);\n", "\tdigitalWrite(1, LOW);\n"])
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: LIGHT takes either ON or OFF as an argument." % i)
                    break
            elif seq[i][pos][1] == 'KEY':
                keystr = "KEY_" + seq[i][pos][0].upper()
                endstr.append(keypress(keystr, defdel))
                break
            elif seq[i][pos][1] == 'MODKEY':
                mkeystr = modconvert(seq[i][pos][0])
                keystr = ""
                for t in seq[i][pos + 1:]:
                    if t[1] == "KEY":
                        keystr += ("KEY_" + t[0].upper() + ",")
                    elif t[1] == "MODKEY":
                        mkeystr += (" | " + modconvert(t[0]))
                    elif t[1] == "STRING":
                        if len(t[0]) == 1:
                            keystr += ("KEY_" + t[0].upper() + ",")
                        else:
                            sys.stderr.write(
                                "Illegal operation on line %d: %s is not a key." % (i, t[0]))
                    else:
                        sys.stderr.write("Illegal operation on line %d." % i)
                if not keystr:
                    keystr = "0,"
                tstr = keystr + " " + mkeystr
                endstr.append(keypress(tstr, defdel))
                break
            else:
                sys.stderr.write("Illegal Opening Command on line %d." % i)
    declist = list(decs)
    return (declist, endstr)


def printparse(seq):
    r = ""
    c = parseseq(seq)
    for i in range(len(c)):
        for j in range(len(c[i])):
            r += c[i][j]
    print r
