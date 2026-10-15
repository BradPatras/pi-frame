# pi-frame

This repo contains my project to create a custom offline digital picture frame using a Raspberry Pi Zero 2W.

### Why Offline?

I think it's annoying when you get a smart device and have to go through a process of connecting it to your home wifi in order to use it. Beyond it being annoying, it also means there's yet another device polluting your wifi, and another entry point for a malicious actor.

### How Do I Add Photos?

This is how the user adds photos to the frame:

1. Click a physical "config" button on the back of the frame
   - This will put the frame into "configuration mode"
2. The frame will start up it's own wifi hotspot and the screen show a wifi network QR code that you can scan with your phone to connect to
3. A second QR code will also be present on the frame's screen that will take you to the configuration page (only accessible on the hotspot)
   - The configuration page lets you modify settings and add/remove photos
4. Pressing the config button again will return the frame to photo display mode and shut down it's hotspot

### Reflections

After finishing the project, I have some thoughts on my approach to it's self-contained functionality and I kinda understand why this isn't a popular way to do smart frames.

The most glaring oversight became obvious immediately when I started testing on the actual hardware. If you connect your phone to the Frame's wifi hotspot, your phone no longer has access to the internet. This is a problem in our current world of cloud-based photo storage. To get around this, you need to pick which photos you want to add, make sure they're downloaded to your phone's storage, THEN you can connect to the frame and upload them. It's not a dealbreaker, but its not great.

The display I chose is another source of slight regret. The frame performed exactly as it should have. The quality looks great, it's bright and it's physically thin. The dev board it came with made it so easy to connect to the raspberry pi. The problem with it is the fact that it's _not_ an OLED. It being an LCD means that black pixels don't actually appear black, they just appear a glowy grey. This is especially glaring because the frame's aspect ratio doesn't match the standard photo aspect ratio, so all photos displayed have ugly greyish black bars along the side. If I had used an OLED, the black pixels would actually be black and would make the whole thing look more polished.

Overall the project worked out really well and I learned a ton about 3D modeling for building the enclosure. Getting all the different aspects of the software working together was also a fun puzzle to figure out. I'll admit I definitely phoned it in with the config interface and a couple of the fields are definitely broken/buggy in it's current state.

### Further info

High level of the pieces involved:

- The photo display is driven by a python script using pygame to render the photos
- The configurator backend server is a python flask app
- The configurator frontend is a react app that is pre-built and pushed to the frame as part of the "deployment". (I will **not** run node on a raspberry pi zero)
- The enclosure was designed in Fusion 360 and 3D printed
- Running on a raspberry pi zero 2w
- The display is from waveshare and cost like 30ish dollars

More info and dev log entries: [dev-docs.md](dev-docs.md)
