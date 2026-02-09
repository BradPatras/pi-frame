#!/bin/bash
# This script is meant to be run on the pi frame once after the code is copied over. 
# It will set up the python environment and install the necessary dependencies.

# Update package lists and install necessary packages
echo "Updating package lists and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip unclutter

# Create a virtual environment and install Python dependencies
echo "Setting up Python virtual environment and installing dependencies..."
python3 -m venv /home/bread/pi-frame/.venv
source /home/bread/pi-frame/.venv/bin/activate
pip install --upgrade pip
pip install -r /home/bread/pi-frame/requirements.txt

# Make scripts executable
chmod +x /home/bread/pi-frame/start-frame.sh
chmod +x /home/bread/pi-frame/start-hotspot.sh
chmod +x /home/bread/pi-frame/stop-hotspot.sh

# Add the photo display service to systemd
echo "Setting up systemd service for the photo display..."
sudo cp /home/bread/pi-frame/photo-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable photo-display.service
sudo systemctl start photo-display.service
