#!/bin/bash

# Disable screen blanking and power saving
xset s off
xset -dpms
xset s noblank

# Hide cursor after 1 second of inactivity
unclutter -idle 1 &

# Start openbox window manager
openbox &

# Wait a moment for openbox to start
sleep 2

# Start the photo display script
/home/bread/frame/.venv/bin/python /home/bread/frame/photo-display-pygame.py
