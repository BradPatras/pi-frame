#!/bin/bash
# $1 is the ssid and $2 is the password
nmcli radio wifi on && sleep 1 && nmcli device wifi hotspot ssid "$1" password "$2"