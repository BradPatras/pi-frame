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

This interface is completely local to the pi.

**implementation**: [`frame-interface/photo_display.py`](frame-interface/photo_display.py)

#### Configuration portal (on frame)

This interface is shown when the frame's physical config button is pressed and contains the following info:

- The frame's wifi network name/password
- The configuration interface web address (could be served up as a QR code alongside the actual address)

**implementation**: [`frame-interface/display_config.py`](frame-interface/display_config.py)

#### Configuration interface (on user device)

This interface is broadcast on the frame's local wifi network and allows modifying the frame's photo contents. The user would use their phone's web browser to access this interface.

Consists following components:

- Inverval adjustment (integer input and dropdown for minutes/hours)
- List of photos currently on-device
  - Each photo should show a small thumbnail, the title, and a trash icon to remove it
- An "Add Photos" button

**Backend implementation**: [`config-interface-backend/server.py`](config-interface-backend/server.py)

**Frontend implementation**: [`config-interface-frontend/`](config-interface-frontend/)

## To do

- [ ] Configuration interface
- [ ] Upload endpoint on server
- [ ] Image resizing before save
- [ ] Custom startup screen (maybe the server will auto-set a random image as the splash screen when photos are added?)
- [x] Autostart script upon boot
- [x] Switch back to headless mode (use openbox?) - full os in cmd line mode

## Logs

### 4/1/26

Got the frame running on the pi zero 2.

it worrrrrrrkkkssssss

Some hurdles
- the venv activate call within the install script doesn't work, needs to be in the start script instead.
- when the start script runs, it shuts off the wifi, which is annoying because i'm ftp-ing to edit files so it needs reset every time
- Found out that the debian network manager basically hard-codes the hotspot hosts ip address so that makes it easier to locate the config interface on the client
- still need to update the frame interface in config mode to show the wifi qr code

### 3/26/26

Trying the wifi hotspot out on a raspberry pi zero _2_. Hopefully the more recent hardware will somehow fix the wifi hotspot issues. Also attempting the 64 bit OS since the more powerful pi should be able to handle it.

Promising! the pi zero 2 running latest 64 bit OS did successfully startup the hotspot AND my android device was able to connect to it!

Now back to the actual frame software...

jk I want some type of build system or task runner in this project to help me remember how to build and package up the project for use on the pi itself.

`just` seems to be a simple easy task runner that'll help me organize the commands I run often.

### 3/18/26

Learned there's a standard for communicating wifi connections via qr code:

> WIFI:T:WPA;S:MyNetwork;P:MyPassword123;;

This means I can communicate both the network and the webpage via qr codes

I downgraded the OS to the previous version (trixie -> bookworm) and viola! the wifi hotspot command worked and I could join the network from my pc. The problem is that I was unable to connect to the hotspot from my android device. My phone kept behaving like I was entering the wrong password.

After some googling I may have found other people reporting the same thing: https://raspberrypi.stackexchange.com/questions/107188/android-wont-connect-to-raspi-access-point

I haven't tried out the suggestions in that thread though.

### 2/9/26

I added an install script because I want to wipe the rpi to start fresh on bookworm instead of trixie (to see if that fixes the hotspot issue).
I realized having the npm build step happen as part of the frame's run script is a terrible idea beacuse that'd mean i'd need to have node and npm installed on the pi and that's a pretty bug lift for that little guy.

So the plan is to prebuild the react app before pushing it to the pi, then just use a simple python server to host it on the pi's local network.

### 2/7/26

I'm attempting to prove out some of this stuff on the actual pi hardware now and immediately hitting a wall with the hotspot part (yikes!). I'm getting this error:

```sh
Error: Connection activation failed: 802.1X supplicant took too long to authenticate
```

seems i'm not the only one: [https://github.com/raspberrypi/trixie-feedback/issues/29](https://github.com/raspberrypi/trixie-feedback/issues/29)

#### 1/29/26

(i'm a dad now)

The frame interface script is now consolidated and also structured as a python class because apparently that's a more idomatic way of doing things. Having functions and raw script in a python file means that if another python file were to attempt to import any of those functions, the file's base level script would auto-run at the import step.

The main py script still needs to be updated to startup the backend and frontend

#### 1/22/26

A lot of the pieces are figured out but I haven't put much thought into how to tie them together. Currently the frame's two "modes" are split into two different python scripts, but that my end up just making things more complicated than they need to be. I think I should either merge them into a single file, or update the python files to be function call-based instead of just a one-shot scripts.

#### 1/12/26

I worked out what the hotspot setup will take. The `network.py` file contains all the info.

#### 1/5/26

After having the frame running for a few days I am noticing that this frame has a blue tint to it. I can modify the images to counteract that using PIL: https://stackoverflow.com/questions/11884544/setting-color-temperature-for-a-given-image-like-in-photoshop

Could be another adjustment on the confg screen "Display color temperature"

Started working on the configuration interface. I'm going with a react app currently (the backend will remain in python though)

#### 1/1/26

Happy new year!

I went ahead with using the full raspi os just set to boot to command line and it worked using the updated service! The script runs on startup and the photos fill the whole display.

#### 12/31/25

I'm now starting the process of switching to headless mode using openbox to create the display window for the pygame to run inside.

Reimaged the pi with the lite os and i'm not sure it's worth it to use lite and then install all the graphical stuff anyway. It might be easier to use the full os and just set it boot to command line...

#### 12/30/25

Originally all of the interfaces were going to just be web pages and yesterday I even got the basic image slideshow working. The issue came when I attempted to run that webpage on the pi zero. Apparently the more recent versions of chromium or rasbian have removed this functionality. Attempting to run anything with chromium gets you this message:

> The hardware on this system lacks support for NEON SIMD extensions.
> We now require NEON or equivalent architecture extensions on ARM-based
> machines. See https://lists.debian.org/debian-devel/2023/09/msg00175.html
> for more information.

Not to mention, many discussions online discuss how a basic web browser needs at least a gigabyte of ram to function. The pi zero has only 512mb of ram.

So with that in mind I'm pivoting to just use python directly to display the fullscreen images. In hindsight using a browser for the image display is massive overkill.

pushing stuff to the display has proved tricky over ssh because it always assumes you're trying to push stuff to the ssh client's display instead of the one plugged into the pi.

I've got it working with tkinter (had to do `export DISPLAY=:0` first) but the photo transitions are kinda rough.

Next I tried using pygame and it seems to be a lot more predictable and smooth. I had to run it with the same display trick, `DISPLAY=:0 python ...` to get anything to appear on the screen, probably because i'm running from ssh.

Pygame seems to work better without any glitchiness when transitioning between images. The next problem to tackle is improving the loading time. The test images i'm using are pretty massive and it takes an extra few seconds to swap between photos because it has to load the next image and scale it down to the display size. I think it'd make the most sense if the server scaled the images as part of the upload process so that when they are saved into the pi's storage, they are already scaled perfectly to fit the display.

Autostart took a bunch of tries because testing reboots is really slow. Initially I was using a crontab job but the script wouldn't work unless the desktop was already loaded so I switched to using a systemd service. This is nice because it only starts after the desktop gui is ready and it'll auto-restart if the script crashes.

```
sudo cp /home/bread/frame/photo-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable photo-display.service
sudo systemctl start photo-display.service
```

#### 12/29/25

I got the initial slideshow of images working using a simple webpage served by a python Flask server.
