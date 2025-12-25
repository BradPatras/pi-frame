# pi-frame

This repo contains a project to create a custom offline digital picture frame using a Raspberry Pi Zero W.

### Why Offline?

I think it's annoying when you get a smart device and have to go through a process of connecting it to your home wifi in order to use it. Beyond it being annoying, it also means there's yet another device polluting your wifi and creating another entry point for malicious actors.

### How Will I Add Photos?

This is how I imagine the user adding photos:

1. Click a "config" button on the frame
    - This will put the frame into "configuration mode"
2. The frame will start up it's own wifi network and the screen show the wifi network name/password, "PI-FRAME", "SOME PASSWORD"
3. A QR code will appear on the frame's screen that will link to a web-page being locally hosted by the frame. This webpage will let the user manage the photos on the frame.
4. After the frame's wifi network has no connections for a certain time period, it will disable the wifi network, returning to its simple image displaying-mode.


## Dev notes

[Headless pi with dispaly output](https://raspberrypi.stackexchange.com/questions/99096/sending-from-headless-raspi-to-hdmi-screen)
