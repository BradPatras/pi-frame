#!/bin/bash

# Disable screen blanking and power saving
xset s off
xset -dpms
xset s noblank

# Hide cursor after 1 second of inactivity
unclutter -idle 1 &

# Start the photo display script
source /home/bread/frame/.venv/bin/activate

/home/bread/frame/.venv/bin/python /home/bread/frame/frame-interface/pi_frame_main.py
