#!/bin/bash
# This script is meant to be run on the pi frame once after the project is copied over. 
# It will set up the python environment, install the necessary dependencies and copy the systemctl service into place.

# Update package lists and install necessary packages
echo "Updating package lists and installing dependencies..."
apt-get update
apt-get install -y python3-venv python3-pip unclutter

# Create a virtual environment and install Python dependencies
echo "Setting up Python virtual environment and installing dependencies..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x start-frame.sh
chmod +x start-hotspot.sh
chmod +x stop-hotspot.sh

# Add the photo display service to systemd
echo "Setting up systemd service for the photo display..."
cp photo-display.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable photo-display.service
systemctl start photo-display.service
