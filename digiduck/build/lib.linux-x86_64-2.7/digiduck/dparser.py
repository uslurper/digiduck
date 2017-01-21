import sys

#Let's define some useful strings

digistr = "DigiKeyboard."

def escstr(string):
    newstr = string.replace('\\','\\\\').replace('"',r'\"').replace('%',r'%%')
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
	endstr = ("for (i=0; i<%s; i++) {\n\t\t" % str(integer-1)) + prev + digidelay(defdel) + "}\n\t"
	return endstr

def modconvert(string):
	if string in ("GUI", "WINDOWS"):
		return "MOD_GUI_LEFT"
	elif string in ("CONTROL", "CTRL"):
		return "MOD_CTRL_LEFT"
	elif string == "ALT":
		return "MOD_ALT_LEFT"
	elif string == "SHIFT":
		return "MOD_SHIFT_LEFT"

def parseblock(seq,ind):
	global defdel
	endstr = ""
	pos = 0
	if ind + 1 == len(seq):
		defdel = 0
	while pos < len(seq[ind]):
		if seq[ind][pos][1] == 'RESERVED':
			if seq[ind][pos][0] == "REM":
				pos += 1
				if seq[ind][pos][1] == "STR":
					endstr += ("// " + seq[ind][pos][0] + "\n")
					break
				else:
					break
			if seq[ind][pos][0] in ("DEFAULT_DELAY","DEFAULTDELAY"):
				pos += 1
				if seq[ind][pos][1] == "INT":
					defdel = int(seq[ind][pos][0])
					break
				else:
					break
			if seq[ind][pos][0] == "DELAY":
				pos += 1
				if seq[ind][pos][1] == "INT":
					endstr += digidelay(int(seq[ind][pos][0]))
					break
				else:
					break
			if seq[ind][pos][0] ==  "STRING":
				pos += 1
				if seq[ind][pos][1] == "STR":
					endstr += digiprint(seq[ind][pos][0], defdel)
					pos += 1
					break
				elif seq[ind][pos][1] == "KEY":
					endstr += keypress(seq[ind][pos][0].upper(), defdel)
					break
				else:
					break
			if seq[ind][pos][0] in ("REPEAT", "REPLAY"):
				pos += 1
				repcount = 0
				if seq[ind][pos][1] == "INT":
					repcount = int(seq[ind][pos][0])
				endstr += repeat(parseblock(seq,ind-1),int(seq[ind][pos][0]), defdel)
				break
		if seq[ind][pos][1] == 'KEY':
			keystr = "KEY_" + seq[ind][pos][0].upper()
			endstr += keypress(keystr,defdel)
			break
		if seq[ind][pos][1] == 'MODKEY':
			mkeystr = modconvert(seq[ind][pos][0])
			keystr = ""
			for t in seq[ind][pos+1:]:
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
