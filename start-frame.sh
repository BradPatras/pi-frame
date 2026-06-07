#!/bin/bash

# Not needed unless running in the desktop environment. Normally this script is run in the terminal on the pi frame
# # Disable screen blanking and power saving
# xset s off
# xset -dpms
# xset s noblank

# # Hide cursor after 1 second of inactivity
# unclutter -idle 1 &

# Start the photo display script
source /home/bread/frame/.venv/bin/activate

startx /home/bread/frame/.venv/bin/python /home/bread/frame/frame-core/pi_frame_main.py
