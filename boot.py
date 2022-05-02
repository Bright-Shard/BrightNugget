import board
from digitalio import DigitalInOut, Pull
from storage import remount, mount, getmount
from json import load, dump

global config
global drive
showBootMenu = False
button = DigitalInOut(board.IO7)
button.switch_to_input(pull=Pull.UP)
showBootMenu = not button.value
drive = getmount('/')

mount(drive, '/', readonly=False)
remount('/', False, disable_concurrent_write_protection=True)

def reset():
    config["Progress Bars"] = True
    config["BeEF Hook URL"] = "https://example.com"
    with open("brightnugget.conf", "w") as configFile:
        dump(config, configFile)
        configFile.close()

try:
    with open("brightnugget.conf", "r") as configFile:
        config = load(configFile)
        configFile.close()
    test = config["Progress Bars"]
    test = config["BeEF Hook URL"]
    test = config["Drive Name"]
except (ValueError, KeyError):
    print("Invalid config, resetting...")
    config = {}
    reset()

drive.label = config["Drive Name"]
with open('loaded', 'w') as file:
    file.write('')
    file.close()


if showBootMenu == True:
    from brightnugget import BrightNugget
    from collections import OrderedDict
    button.deinit()

    class BootMenu(BrightNugget):
        def __init__(self):
            super().__init__()

            bootMenuList = OrderedDict(
                [
                    ("Reset BrightNugget Config", reset),
                    ("Boot", self.boot),
                ]
            )
            self.bootMenu = self.guiList("Boot Menu", bootMenuList)
            self.bootMenu.show()

        def saveConfig(self):
            with open("brightnugget.conf", "w") as configFile:
                dump(config, configFile)
                configFile.close()

        def boot(self):
            self.stop = True

    BootMenu()
