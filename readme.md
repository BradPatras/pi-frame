# pi-frame

This repo contains a project to create a custom offline digital picture frame using a Raspberry Pi Zero W.

### Why Offline?

I think it's annoying when you get a smart device and have to go through a process of connecting it to your home wifi in order to use it. Beyond it being annoying, it also means there's yet another device polluting your wifi, another entry point for malicious actors and potentially it may introduce the need for a paid service of some kind.

### How Will I Add Photos?

This is how I imagine the user adding photos:

1. Click a physical "config" button on the frame
   - This will put the frame into "configuration mode"
2. The frame will start up it's own wifi network and the screen show the wifi network name/password, "PI-FRAME", "SOME PASSWORD"
3. A QR code will appear on the frame's screen that will link to a web-page being locally hosted by the frame. This webpage will let the user manage the photos on the frame.
4. After the frame's wifi network has no connections for a certain time period, it will disable the wifi network, returning to its simple image displaying-mode. (Pressing the config button again will also return to picture mode)

## Hardware

### Board

- Raspberry pi zero w
  - I could definitely get away with using a microcontroller instead of an SBC but I'm mostly worried about the web server/image uploading step and I know a rpi will have the power to do it.

### Display

Could go with gpio pased display or hdmi.
(hdmi seems simpler since raspberry pi has the port)

- The random display I bought from amazon for dev:
  - 7 inch hdmi-based ips: https://a.co/d/9zcXfZG
    - $34.99
- Waveshare has tons of options:
  - 7 inch gpio-based ips: https://www.waveshare.com/7inch-lcd-for-pi.htm
    - $29.99
  - 7 inch hdmi-based ips: https://www.waveshare.com/product/7inch-hdmi-lcd.htm
    - $43.99
  - 7 inch hdmi-based (via converter board) ips: https://www.waveshare.com/70h-1024600.htm?sku=22672
    - $33.99 with (converter board included)

## Dev notes

[Headless pi with display output](https://raspberrypi.stackexchange.com/questions/99096/sending-from-headless-raspi-to-hdmi-screen)
[Installing basics required to push stuff to a display without a desktop environment](https://raspberrypi.stackexchange.com/a/66594)

using a python flask app for the backend. This should make it easy to interface with the PI's gpio for the button presses.
To start the local server, run:

```sh
gunicorn -w 2 -b 0.0.0.0:8000 server:app
```

### Main components

#### Photo display interface (on frame)

This interface occupies the whole frame display and shows the images one by one, switching between them according to a set time interval (8 hours, for example).

This interface can be completely local to the pi.

#### Configuration portal (on frame)

This interface is shown when the frame's physical config button in pressed and contains the following info:

- The frame's wifi network name/password
- The configuration interface web address (could be served up as a QR code alongside the actual address)

#### Configuration interface (on user device)

This interface is broadcast on the frame's local wifi network and allows modifying the frame's photo contents. The user would use their phone's web browser to access this interface.
