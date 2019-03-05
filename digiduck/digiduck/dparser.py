import sys

#This is mostly to help me stay sane while writing all of these strings.
digistr = "DigiKeyboard."

def escstr(string):
    #This function takes in a string and helpfully escapes it for use in the final program.
    newstr = string.replace('\\', '\\\\').replace('"', r'\"').replace('%', r'%%')
    return newstr

def autoindent(strlist):
    #This function is pretty straightforward, it takes a list of strings and indents them all to use inside of a nested scope.
    result = []
    for line in strlist:
        result.append("\t" + line)
    return result

def abstractdelay():
    #This just creates a function definition when needed to minimize the size of generated code.
    return "void digidelay(int n) {\n\n\t" + digistr + "delay(n);\n\t" + digistr + "sendKeyStroke(0);\n\n}\n\n"

def digidelay(integer):
    #This function inserts a delay into the resulting program when desired.
    if integer == 0:
        return [""]
    return ["\t" + ("digidelay(%d)" % integer) + ";\n"]

def abstractprint(defdel):
    #This just creates a function definition when needed to minimize the size of generated code.
    return "void digiprint(String s) {\n\n\t" + digistr + ("println(s);\n\tdigidelay(%d);" % defdel) + "\n\n}\n\n"

def digiprint(string):
    #This function tells the digispark to type a given string.
    r = ["\t" + ("digiprint(\"%s\")" % escstr(string)) + ";\n"]
    return r

def abstractkeypress(defdel):
    #This just creates a function definition when needed to minimize the size of generated code.
    return "void digikeypress(String s) {\n\n\t" + digistr + ("sendKeyStroke(s);\n\tdigidelay(%d);" % defdel) + "\n\n}\n\n"

def keypress(keys):
    #This function tells the digispark to simulate a given keystroke.
    r = ["\t" + ("digikeypress(%s)" % keys) + ";\n"]
    return r


def repeat(prev, integer, lev):
    #This function creates a for loop in the resulting code containing the instructions specified in the initial file.
    p = []
    for l in prev:
        if l != [""]:
            #We only add an instruction if it isn't blank
            p.append(l)
    body = ["\tfor (uint8_t i%d=0; i%d<%d; i%d++) {\n" % (lev, lev, integer, lev)]
    body.extend(autoindent(p))
    body.append("\t}\n")
    return body


def modconvert(string):
    #These are just helpful conversions to get the digispark to press the right key.
    if string in ("GUI", "WINDOWS"):
        return "MOD_GUI_LEFT"
    elif string in ("CONTROL", "CTRL"):
        return "MOD_CTRL_LEFT"
    elif string == "ALT":
        return "MOD_ALT_LEFT"
    elif string == "SHIFT":
        return "MOD_SHIFT_LEFT"


def parseseq(seq):
    #This function does almost all of the work of this entire program. I'll try annotating everything that might be confusing.
    #First, we state that we haven't introduced any helper functions.
    addeclared = False
    apdeclared = False
    akpdeclared = False
    #Now we make an array for those functions if we need them.
    functions = []
    #Now we create a place for code to be inserted in the setup function.
    setup = []
    #Now a place for the loop function.
    loops = []
    #Finally, a place for general setup instructions where the order of execution is entirely unimportant, but shouldn't have repeated elements. Might merge this with setup eventually, but this helps with refactoring.
    decs = set()
    #We set our scope level to help with nested loops.
    lev = 0
    i = 0
    while i < len(seq):
        #If we're just starting our iteration through the token list, we want to initialize our default delay to zero.
        if i == 0:
            defdel = 0
        pos = 0
        #We introduce a temporary delay variable, in case the default delay is assigned multiple times.
        tdel = defdel
        #If the token list is entirely expended, we set our default delay to 0. I'm not sure why this is here, but whenever I think that and get rid of something my life gets noticeably harder.
        if i + 1 == len(seq):
            defdel = 0
        #We're going to be modifying our line position liberally during this loop, so we need to use a while block instead of a for loop.
        while pos < len(seq[i]):
            #Check to see if the program should be doing something
            if seq[i][pos][1] == 'RESERVED':
                #If there's a comment in the duckyscript, it should be a comment in the digispark code.
                if seq[i][pos][0] == "REM":
                    for t in range(1, len(seq[i])):
                        com = ""
                        com += seq[i][pos + t][0]
                    setup.extend(["\t// " + com + "\n"])
                    i += 1
                    break
                #If the user specifies a default delay, that should be maintained throughout the program.
                elif seq[i][pos][0] in ("DEFAULT_DELAY", "DEFAULTDELAY"):
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        defdel = int(seq[i][pos][0])
                        i += 1
                        break
                    else:
                        #You might be wondering why I allow execution to continue even when certain lines are not parseable. This is because broken spaghetti code builds character and might teach people to read the documentation.
                        sys.stderr.write(
                            "Illegal Op on line %d: DEFAULTDELAY takes an integer argument." % i)
                        i += 1
                        break
                #If the user wants to insert a delay, we should create a helper function to do that so we don't repeat ourselves.
                elif seq[i][pos][0] == "DELAY":
                    pos += 1
                    if seq[i][pos][1] == "INT":
                        #Check if we already have that function first.
                        if not addeclared:
                            functions.append(abstractdelay())
                            addeclared = True
                        setup.extend(digidelay(int(seq[i][pos][0])))
                        i += 1
                        break
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: DELAY takes an integer argument." % i)
                        i += 1
                        break
                #If the user wants to type/press something, we should let them.
                elif seq[i][pos][0] == "STRING":
                    pos += 1
                    if seq[i][pos][1] == "STR":
                        #Check if we have the appropriate helper function first.
                        if not apdeclared:
                            functions.append(abstractprint(defdel))
                            apdeclared = True
                        setup.extend(digiprint(seq[i][pos][0]))
                        pos += 1
                        i += 1
                        break
                    elif seq[i][pos][1] == "KEY":
                        #Check if we have a function for this.
                        if not akpdeclared:
                            functions.append(abstractkeypress(defdel))
                            akpdeclared = True
                        setup.extend(keypress(seq[i][pos][0].upper()))
                        i += 1
                        break
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: STRING takes a string argument." % i)
                        i += 1
                        break
                #Here's where things get a little dense.
                elif seq[i][pos][0] in ("REPEAT", "REPLAY"):
                    #Move to the first argument, initialize our loop length, and make a space for our looped instructions.
                    pos += 1
                    repcount = 0
                    prev = []
                    lcount = 1
                    #If there's no second parameter, assume we're just repeating the previous instruction.
                    if len(seq[i]) == 2:
                        if seq[i][pos][1] == "INT":
                            repcount = int(seq[i][pos][0])
                        else:
                            sys.stderr.write(
                                "Illegal Op on line %d: REPEAT takes integer args." % i)
                        prev.append(setup[i - 1])
                    elif len(seq[i]) == 3:
                        if seq[i][pos][1] == "INT":
                            #This is the number of lines we're repeating.
                            lcount = int(seq[i][pos][0])
                            pos += 1
                            if seq[i][pos][1] == "INT":
                                #This is the number of times to repeat those lines.
                                repcount = int(seq[i][pos][0])
                            else:
                                sys.stderr.write(
                                    "Illegal Op on line %d: REPEAT takes integer args." % i)
                            for j in range(lcount, 0, -1):
                                #Instead of trying to parse the prior instructions in a subprocess, we just take them from what we've already parsed.
                                prev.append(setup[i - j - 1])
                        else:
                            sys.stderr.write(
                                "Illegal Op on line %d: REPEAT takes integer args." % i)
                    else:
                        sys.stderr.write("Illegal Syntax on line %d: REPEAT takes 1-2 args.")
                    tls = repeat(prev, repcount, lev)
                    lev += 1
                    #Here we're just making sure the line counts sync up for debug messages. This is probably unnecessary, honestly, but I'm unwilling to find out at this time.
                    for j in range(lcount):
                        setup.pop()
                    for j in range(lcount):
                        setup.extend([""])
                    setup.extend(tls)
                    i += 1
                    break
                #Here, we start getting into looping behavior.
                #First, check if the user wants to trigger something repeatedly.
                elif seq[i][pos][0] == "RTRIGGER":
                    if len(seq[i]) != 1:
                        loopbody = []
                        pos += 1
                        #Check if our parameter is of the right type first.
                        if seq[i][pos][1] == "INT" or seq[i][pos][1] == "FLOAT":
                            freq = float(seq[i][pos][0])
                            if freq != 100:
                                scaled = int(freq * 100)
                            else:
                                scaled = 10000
                            if len(seq[i]) == 3:
                                if seq[i][pos + 1][1] == "TIME":
                                    #If we have a time-format parameter, scale it to milliseconds.
                                    muldict = {
                                    "s": 1000,
                                    "m": 60 * 1000,
                                    "h": 60 * 60 * 1000,
                                    "d": 24 * 60 * 60 * 1000
                                    }
                                    val = int(seq[i][pos + 1][0][:-1])
                                    mul = muldict[seq[i][pos + 1][0][-1]]
                                    loopbody.extend(digidelay(val * mul))
                                elif seq[i][pos + 1][1] == "INT":
                                    #If just a number is given, use it as the milliseconds.
                                    loopbody.extend(digidelay(int(seq[i][pos + 1][0])))
                                else:
                                    sys.stderr.write("RTRIGGER takes an integer or time-format delay argument. (ns, nm, nh, nd)")
                            else:
                                #Default to 1s delay time
                                loopbody.extend(digidelay(1000))
                            #Set up our random test and the conditional block if they don't want to run the code 100% of the time.
                            if scaled != 10000:
                                loopbody.append("\n\tuint16_t r = random(10000);\n\n\tif (r <= %d) {\n\n" % scaled)
                            interior = []
                            i += 1
                            try:
                                #Get the next instructions up to the block terminator
                                while seq[i][0][0] != "ENDR":
                                    interior.append(seq[i])
                                    i += 1
                            except IndexError:
                                #If the user forgot to end their block, chide them a bit.
                                sys.stderr.write("No ENDR encountered to terminate random trigger.")
                                i += 1
                                break
                            #Let's not write the previous instructions twice.
                            i += len(interior) - 1
                            #Here we parse the instructions we want to put in our loop function, then insert the generated code in the right places.
                            parsed = parseseq(interior)
                            functions.extend(parsed[0])
                            functions = list(set(functions))
                            newdecs = decs.union(set(parsed[1]))
                            decs = newdecs
                            #If the code isn't supposed to run every time, we wrap it in a deeper scope.
                            if scaled != 10000:
                                loopbody.append("".join(autoindent(parsed[2])))
                                loopbody.append("\n\t}\n")
                            else:
                                loopbody.append("".join(parsed[2]))
                            loops.append("".join(loopbody))
                            break
                        else:
                            sys.stderr.write("RTRIGGER takes an integer frequency param.")
                        i += 1
                        break
                    else:
                        sys.stderr.write("RTRIGGER takes at least one argument.")
                        i += 1
                        break
                #If the user wants to trigger the onboard LED, we need to set the pins appropriately before using those instructions.
                elif seq[i][pos][0] == "LIGHT":
                    pos += 1
                    decs.add("\tpinMode(0, OUTPUT);\n")
                    decs.add("\tpinMode(1, OUTPUT);\n")
                    if seq[i][pos][0] == "ON":
                        setup.extend(["\tdigitalWrite(0, HIGH);\n", "\tdigitalWrite(1, HIGH);\n"])
                    elif seq[i][pos][0] == "OFF":
                        setup.extend(["\tdigitalWrite(0, LOW);\n", "\tdigitalWrite(1, LOW);\n"])
                    else:
                        sys.stderr.write(
                            "Illegal Op on line %d: LIGHT takes either ON or OFF as an argument." % i)
                    i += 1
                    break
            #If the user wants to press a particular key, we need the right instruction to pass.
            elif seq[i][pos][1] == 'KEY':
                keystr = "KEY_" + seq[i][pos][0].upper()
                if not akpdeclared:
                    functions.append(abstractkeypress(defdel))
                    akpdeclared = True
                setup.extend(keypress(keystr))
                i += 1
                break
            #If the user wants to press a modkey, the instruction is a bit different, since it will usually be used in conjunction with other keys.
            elif seq[i][pos][1] == 'MODKEY':
                #Modkey instructions have to be passed as the final parameter in the keypress instruction, with binary "or" applied between it and the other modkeys.
                mkeystr = modconvert(seq[i][pos][0])
                keystr = ""
                for t in seq[i][pos + 1:]:
                    if t[1] == "KEY":
                        keystr += ("KEY_" + t[0].upper() + ",")
                    elif t[1] == "MODKEY":
                        mkeystr += (" | " + modconvert(t[0]))
                    elif t[1] == "STRING":
                    #This conditional is mostly to catch any potential error where a key is misidentified as a string.
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
                if not akpdeclared:
                    functions.append(abstractkeypress(defdel))
                    akpdeclared = True
                setup.extend(keypress(tstr))
                i += 1
                break
            else:
                sys.stderr.write("Illegal Opening Command on line %d." % i)
    #We return our setup instructions as a list to make appending them to the output a little easier.
    declist = list(decs)
    return (functions, declist, setup, loops)
