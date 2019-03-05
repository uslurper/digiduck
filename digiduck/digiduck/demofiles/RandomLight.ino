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

void setup() {

	pinMode(0, OUTPUT);
	pinMode(1, OUTPUT);

}

void loop() {

	digidelay(10000);
	digitalWrite(0, HIGH);
	digitalWrite(1, HIGH);
	digidelay(1000);
	digitalWrite(0, LOW);
	digitalWrite(1, LOW);


}