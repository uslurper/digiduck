import sys

# Let's define some useful strings

digistr = "DigiKeyboard."


def escstr(string):
    newstr = string.replace('\\', '\\\\').replace('"', r'\"').replace('%', r'%%')
    return newstr


def digidelay(integer):
    if integer == 0:
        return ""
    return digistr + ("delay(%d)" % integer) + ";\n\tDigiKeyboard.sendKeyStroke(0);\n\t"


def digiprint(string, defdel):
    return digistr + ("println(\"%s\")" % escstr(string)) + ";\n\t" + digidelay(defdel)


def keypress(keys, defdel):
    return digistr + ("sendKeyStroke(%s)" % keys) + ";\n\t" + digidelay(defdel)


def repeat(prev, integer, defdel):
    if digidelay(defdel):
        delayls = digidelay(defdel).split("\t")
        delayls[0] += "\t\t"
        delayls[1] += "\t"
        delaystr = delayls[0] + delayls[1]
    else:
        delaystr = ""
    prevstr = ""
    for line in prev:
        if ".delay(" in line:
            tls = line.split("\t")
            tls[0] += "\t\t"
            tls[1] += "\t"
            line = tls[0] + tls[1]
        prevstr += (line + "\t" + delaystr)
    endstr = ("for (i=0; i<%s; i++) {\n\t\t" % str(integer)) + prevstr[:-1] + "}\n\t"
    return endstr


def modconvert(string):
    if string in ("GUI", "WiOWS"):
        return "MOD_GUI_LEFT"
    elif string in ("CONTROL", "CTRL"):
        return "MOD_CTRL_LEFT"
    elif string == "ALT":
        return "MOD_ALT_LEFT"
    elif string == "SHIFT":
        return "MOD_SHIFT_LEFT"


def parseblock(seq, i, endstr, defdel):
    pos = 0
    while pos < len(seq[i]):
        if seq[i][pos][1] == 'RESERVED':
            if seq[i][pos][0] == "REM":
                pos += 1
                if seq[i][pos][1] == "STR":
                    endstr += ("// " + seq[i][pos][0] + "\n\t")
                    break
                else:
                    break
            if seq[i][pos][0] in ("DEFAULT_DELAY", "DEFAULTDELAY"):
                pos += 1
                if seq[i][pos][1] == "INT":
                    defdel = int(seq[i][pos][0])
                    break
                else:
                    break
            if seq[i][pos][0] == "DELAY":
                pos += 1
                if seq[i][pos][1] == "INT":
                    endstr += digidelay(int(seq[i][pos][0]))
                    break
                else:
                    break
            if seq[i][pos][0] == "STRING":
                pos += 1
                if seq[i][pos][1] == "STR":
                    endstr += digiprint(seq[i][pos][0], defdel)
                    pos += 1
                    break
                elif seq[i][pos][1] == "KEY":
                    endstr += keypress(seq[i][pos][0].upper(), defdel)
                    break
                else:
                    break
            if seq[i][pos][0] in ("REPEAT", "REPLAY"):
                pos += 1
                repcount = 0
                prev = []
                if len(seq[i]) == 2:
                    if seq[i][pos][1] == "INT":
                        repcount = int(seq[i][pos][0])
                    prev.append(parseblock(seq, i - 1))
                elif len(seq[i]) == 3:
                    if seq[i][pos][1] == "INT":
                        lcount = int(seq[i][pos][0])
                        pos += 1
                        if seq[i][pos][1] == "INT":
                            repcount = int(seq[i][pos][0])
                        for j in range(lcount, 0, -1):
                            prev.append(parseblock(seq, i - j))
                endstr = endstr[:-len("".join(prev))]
                endstr += repeat(prev, int(repcount), tdel)
                break
        if seq[i][pos][1] == 'KEY':
            keystr = "KEY_" + seq[i][pos][0].upper()
            endstr += keypress(keystr, defdel)
            break
        if seq[i][pos][1] == 'MODKEY':
            mkeystr = modconvert(seq[i][pos][0])
            keystr = ""
            for t in seq[i][pos + 1:]:
                if t[1] == "KEY":
                    keystr += ("KEY_" + t[0].upper() + ",")
                elif t[1] == "MODKEY":
                    mkeystr += (" | " + modconvert(t[0]))
                else:
                    sys.stderr.write("Illegal operation on line %d" % i)
            if not keystr:
                keystr = "0,"
            tstr = keystr + " " + mkeystr
            endstr += keypress(tstr, defdel)
            break
    return endstr


def parseseq(seq):
    endstr = ""
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
                    pos += 1
                    if seq[i][pos][1] == "STR":
                        endstr += ("// " + seq[i][pos][0] + "\n\t")
                        break
                    else:
                        break
                if seq[i][pos][0] in ("DEFAULT_DELAY", "DEFAULTDELAY"):
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        defdel = int(seq[i][pos][0])
                        break
                    else:
                        break
                if seq[i][pos][0] == "DELAY":
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        endstr += digidelay(int(seq[i][pos][0]))
                        break
                    else:
                        break
                if seq[i][pos][0] == "STRING":
                    pos += 1
                    if seq[i][pos][1] == "STR":
                        endstr += digiprint(seq[i][pos][0], defdel)
                        pos += 1
                        break
                    elif seq[i][pos][1] == "KEY":
                        endstr += keypress(seq[i][pos][0].upper(), defdel)
                        break
                    else:
                        break
                if seq[i][pos][0] in ("REPEAT", "REPLAY"):
                    pos += 1
                    repcount = 0
                    prev = []
                    if len(seq[i]) == 2:
                        if seq[i][pos][1] == "INT":
                            repcount = int(seq[i][pos][0])
                        prev.append(parseblock(seq, i - 1, "", defdel))
                    elif len(seq[i]) == 3:
                        if seq[i][pos][1] == "INT":
                            lcount = int(seq[i][pos][0])
                            pos += 1
                            if seq[i][pos][1] == "INT":
                                repcount = int(seq[i][pos][0])
                            for j in range(lcount, 0, -1):
                                prev.append(parseblock(seq, i - j, "", defdel))
                    endstr = endstr[:-len("".join(prev))]
                    endstr += repeat(prev, int(repcount), tdel)
                    break
            if seq[i][pos][1] == 'KEY':
                keystr = "KEY_" + seq[i][pos][0].upper()
                endstr += keypress(keystr, defdel)
                break
            if seq[i][pos][1] == 'MODKEY':
                mkeystr = modconvert(seq[i][pos][0])
                keystr = ""
                for t in seq[i][pos + 1:]:
                    if t[1] == "KEY":
                        keystr += ("KEY_" + t[0].upper() + ",")
                    elif t[1] == "MODKEY":
                        mkeystr += (" | " + modconvert(t[0]))
                    else:
                        sys.stderr.write("Illegal operation on line %d" % ind)
                if not keystr:
                    keystr = "0,"
                tstr = keystr + " " + mkeystr
                endstr += keypress(tstr, defdel)
                break
    return endstr
