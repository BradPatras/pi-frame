import os
import subprocess

# This explains how i'll be able to run nmcli commands without being prompted for a password
# https://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password/155827#155827
# After those steps are taken, the following sudo calls should work without a password prompt


def enable_wifi_hotspot(ssid, password):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["bash", "../start-hotspot.sh", ssid, password], cwd=script_dir)


def disable_wifi_hotspot():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["bash", "../stop-hotspot.sh"], cwd=script_dir)
