# Ducktor, Rubberduck and CnC Server

<img src="https://raw.githubusercontent.com/IngvarOlsen/RubberDuckyCnC/main/ducktor/static/ducktor.png" width="300">

## About

School IoT project where we were building a rubberduck(Bad USB) with a Raspberry Pi Zero 2 W, and a virus Command and dashboard server in flask. We also explored ways to safeguard against it. The idea was to make a starting point for a Raspberry Pi Zero powered rubber duck with the possibility to pivot over to capabilities like FlipperZero, and help pen testers and companies to make a user specific mockup python virus which could simulate different types of virus behavior. The project is in early stages and can compile a Windows virus from a Windows machine, but it should be possible to compile from a linux machine with a docker container with Wine running. The Rubberduck side of the project comes with a separate flask application for settings to select a rubberduck script to run and if it should be run on boot or looped. The project is kind of rough and still in dvelopment, the virus right now only shows Ip, Windows and some hardware info. Future plans including making it possible to simulate a wide range of malware activity such as fake ransomeware.

Main server is main.py and the Rubberduck solution is inside the ducktor folder, and is run with app.py

The raspberry Pi must also have been set up as a HID Gadget and the app.py run on boot. The App.py also most likely only works with Danish keyboards, and is not fully mapped. Encountered a problem where the keys from the danish Ubuntu keyboard was offset from the Danish keyboard on the target computer so had to do some manual mapping and only mapped the keys we are using for the rubberduck scripts.

Tutorial for setting up Pi as HID Gadget: https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/

The python file can be called before "exit 0" in the /etc/rc.local file after the HID gadget

Also secrets are not so secret in this project atm, propper .env file will be made.

Files with "_old." are files which is as they were as the project was handed in and have been made as a copy to continue development.

## Requirements

Pip libraries you need to run this project. To install them, you can use pip:

```bash
pip install -r requirements.txt
