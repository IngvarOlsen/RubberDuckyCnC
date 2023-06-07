# Ducktor, Rubberduck and CnC Server

<img src="https://raw.githubusercontent.com/IngvarOlsen/RubberDuckyCnC/main/ducktor/static/ducktor.png" width="300">

## About

School IoT project where we were building a rubberduck(Bad USB) with a Raspberry Pi Zero 2 W, and a virus Command and dashboard server in flask. We also explored ways to safeguard against it. The idea was to make a starting point for a Raspberry Pi Zero powered rubber duck with the possibility to pivot over to capabilities like FlipperZero, and help pen testers and companies to make a user specific mockup python virus which could simulate different types of virus behavior. The project is in early stages and can compile a Windows virus from a Windows machine, but it should be possible to compile from a linux machine with a docker container with Wine running. The Rubberduck side of the project comes with a separate flask application for settings to select a rubberduck script to run and if it should be run on boot or looped. The virus right now only shows Ip, Windows and some hardware info.

## Requirements

Pip libraries you need to run this project. To install them, you can use pip:

```bash
pip install -r requirements.txt
