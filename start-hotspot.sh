#!/bin/bash
# $1 is the ssid and $2 is the password
nmcli radio wifi on && nmcli device wifi hotspot ssid "$1" password "$2"