# About BrightNugget
BrightNugget is my twist on HID attacks with the Wifi Nugget by Retia(See their
[Github Profile](https://github.com/HakCat-Tech)). It automates some tasks in HID attacks (Opening the terminal or other
apps, for example), includes a few pranks, and (most importantly), allows basic GUIs to be built on the nugget with
list-based interfaces. This allows for many payloads to be stored on one nugget, instead of having 15 microSD
cards for something like the USB Rubber Ducky.

# Notice
I've not written programs in CircuitPython before this project. If you see any obvious errors or areas I can improve
this program, open a pull request or GitHub issue. Feedback is appreciated!

# Installation
For the basic libraries, copy the code from `/lib` onto the `lib` folder of your Wifi Nugget. BrightNugget also needs
a few libraries from the CircuitPython default libraries (you can get them 
[here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)):
- `adafruit_display_text`: Used for showing text on the Wifi Nugget
- `adafruit_hid`: This performs the actual HID attacks
- `adafruit_progressbar`: Because yes, I was extra and included progress bars. These can be disabled.
- `adafruit_debouncer.mpy`: For using the buttons on the Wifi Nugget
- `adafruit_displayio_sh1106.mpy`: For controlling the screen. **Adafruit has multiple libraries for controlling
different types of screens. Make sure to get the `sh1106` library.**

In addition, I have written an example BrightNugget setup. To use it, copy the `code.py` and `boot.py` files to your
Wifi Nugget. The `brightnugget.conf` file is used by my example BrightNugget setup (it's not needed by the libraries)
and is automatically generated when an invalid (or lack of) configuration is detected. (Tl;DR: You don't need to copy
the `brightnugget.conf` file over.)

# Documentation
Coming soon™.