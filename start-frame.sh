#!/bin/bash

# Disable screen blanking and power saving
xset s off
xset -dpms
xset s noblank

# Hide cursor after 1 second of inactivity
unclutter -idle 1 &

# Start the photo display script
/home/bread/pi-frame/.venv/bin/python /home/bread/pi-frame/photo-display-pygame.py
