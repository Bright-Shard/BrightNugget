import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Pull
from collections import OrderedDict
import adafruit_displayio_sh1106
from adafruit_progressbar.progressbar import HorizontalProgressBar


class BrightNugget:
    def __init__(self):
        displayio.release_displays()
        self.display = adafruit_displayio_sh1106.SH1106(
            displayio.I2CDisplay(busio.I2C(board.SCL, board.SDA), device_address=0x3C),
            width=130,
            height=64,
        )
        self.buttonManager = ButtonManager()
        self.currentDisplay = None
        self.stop = False

    def setKeybinds(self, binds: dict):
        self.buttonManager.left = binds["Left"]
        self.buttonManager.right = binds["Right"]
        self.buttonManager.up = binds["Up"]
        self.buttonManager.down = binds["Down"]

    def switchMenu(self, menu):
        if self.currentDisplay is not None:
            self.stop = True
        self.display.show(menu)
        self.currentDisplay = menu
        if callable(menu.onOpen):
            try:
                menu.onOpen()
            except TypeError as e:
                menu.onOpen(None)
        self.loop()

    def loop(self):
        while True:
            if self.stop is True:
                self.stop = False
                break
            self.buttonManager.update()
            self.display.refresh()

    def guiList(self, title: str, options: dict, onOpen=None):
        return GUIList(title, options, self, onOpen)

    def guiProgressBar(self, back: GUIList, onOpen=None):
        return GUIProgressBar(back, self, onOpen)

    def guiMessage(self, title: str, message: str, back: GUIList, onOpen=None):
        return GUIMessage(title, message, back, self, onOpen)


class ButtonManager:
    def __init__(self):
        upButton = DigitalInOut(board.IO9)
        downButton = DigitalInOut(board.IO18)
        leftButton = DigitalInOut(board.IO11)
        rightButton = DigitalInOut(board.IO7)

        upButton.pull = Pull.UP
        downButton.pull = Pull.UP
        leftButton.pull = Pull.UP
        rightButton.pull = Pull.UP

        self.up = None
        self.down = None
        self.left = None
        self.right = None

        self.buttons = [
            Debouncer(upButton),
            Debouncer(downButton),
            Debouncer(leftButton),
            Debouncer(rightButton),
        ]

    def update(self):
        funcs = [self.up, self.down, self.left, self.right]
        for i in range(0, 4):
            self.buttons[i].update()
            if self.buttons[i].fell and funcs[i] is not None:
                funcs[i]()


class GUIList(displayio.Group):
    def __init__(
        self,
        title: str,
        options: OrderedDict,
        nugget: BrightNugget,
        onOpen=None,
    ):
        super().__init__()
        self.options = options
        self.back = self
        self.selection = 1
        self.optionsCount = 0
        self.minOption = 1
        self.maxOption = 4
        self.nugget = nugget
        self.onOpen = onOpen

        self.append(
            label.Label(
                terminalio.FONT,
                text=title,
                x=5,
                y=5,
                padding_left=2,
                padding_right=2,
                padding_top=-2,
                color=0xFFFFFF,
                background_color=0x000000,
            )
        )
        for option in options:
            self.append(
                label.Label(
                    terminalio.FONT,
                    text=str(self.optionsCount + 1) + ". " + option,
                    x=5,
                    y=(12 * (self.optionsCount + 1)) + 5,
                    padding_left=2,
                    padding_right=2,
                    padding_top=-2,
                    color=0xFFFFFF,
                    background_color=0x000000,
                )
            )
            self.optionsCount += 1
        self.options = list(self.options.values())
        if self.optionsCount < 4:
            self.maxOption = self.optionsCount

        self[self.selection].color = 0x000000
        self[self.selection].background_color = 0xFFFFFF

    def up(self):
        if self.selection == self.minOption and self.minOption > 1:
            for i in range(1, len(self)):
                item = self[i]
                newY = item.y + 12
                if newY == 2:
                    newY = 17
                item.y = newY
            self.minOption -= 1
            self.maxOption -= 1

        self[self.selection].color = 0xFFFFFF
        self[self.selection].background_color = 0x000000
        if self.selection > self.minOption:
            self.selection -= 1
        elif self.selection == 1:
            self.selection = self.maxOption
        self[self.selection].color = 0x000000
        self[self.selection].background_color = 0xFFFFFF

    def down(self):
        if self.selection == self.maxOption and self.maxOption < (len(self) - 1):
            for i in reversed(range(1, len(self))):
                item = self[i]
                newY = item.y - 12
                if newY == 5:
                    newY = -10
                item.y = newY
            self.minOption += 1
            self.maxOption += 1

        self[self.selection].color = 0xFFFFFF
        self[self.selection].background_color = 0x000000
        if self.selection < self.maxOption:
            self.selection += 1
        elif self.selection == (len(self) - 1):
            self.selection = self.minOption
        self[self.selection].color = 0x000000
        self[self.selection].background_color = 0xFFFFFF

    def run(self):
        toRun = self.options[self.selection - 1]
        if type(toRun) is GUIList:
            toRun.back = self
            toRun.show()
        elif callable(toRun):
            try:
                toRun()
            except TypeError as error:
                toRun(None)

    def show(self):
        if callable(self.onOpen):
            try:
                self.onOpen()
            except TypeError:
                self.onOpen(None)
        self.nugget.setKeybinds(
            {
                "Up": self.up,
                "Down": self.down,
                "Left": self.back.show,
                "Right": self.run,
            }
        )
        self.nugget.switchMenu(self)


class GUIProgressBar(displayio.Group):
    def __init__(
        self,
        back: GUIList,
        nugget: BrightNugget,
        onOpen=None,
    ):
        super().__init__()
        self.back = back
        self.nugget = nugget
        self.onOpen = onOpen

        self.label = label.Label(
            terminalio.FONT,
            text="",
            x=5,
            y=5,
            padding_left=2,
            padding_right=2,
            padding_top=-2,
            color=0xFFFFFF,
            background_color=0x000000,
        )
        self.progressbar = HorizontalProgressBar(
            (5, 17),
            (120, 30),
            bar_color=0xFFFFFF,
            outline_color=0xFFFFFF,
            fill_color=0x000000,
            value=0,
        )
        self.finished = label.Label(
            terminalio.FONT,
            text="Hit the right arrow\nto continue",
            x=5,
            y=35,
            padding_left=2,
            padding_right=2,
            padding_top=-2,
            color=0xFFFFFF,
            background_color=0x000000,
            scale=1,
            line_spacing=0.8,
        )

        self.append(self.label)
        self.append(self.progressbar)

    def changeText(self, text: str):
        self.label.text = text

    def changePercent(self, percent: int):
        self.progressbar.value = percent
        if percent is 100:
            self.pop(1)
            self.append(self.finished)
            self.showFinished()

    def reset(self):
        self.pop(1)
        self.append(self.progressbar)
        self.progressbar.value = 0

    def show(self):
        if callable(self.onOpen):
            try:
                self.onOpen()
            except TypeError:
                self.onOpen(None)
        self.nugget.setKeybinds(
            {
                "Up": None,
                "Down": None,
                "Left": None,
                "Right": None,
            }
        )
        self.nugget.switchMenu(self)

    def showFinished(self):
        self.nugget.setKeybinds(
            {
                "Up": self.back.show,
                "Down": self.back.show,
                "Left": self.back.show,
                "Right": self.back.show,
            }
        )
        self.nugget.switchMenu(self)


class GUIMessage(displayio.Group):
    def __init__(
        self,
        title: str,
        message: str,
        back: GUIList,
        nugget: BrightNugget,
        onClose=None,
    ):
        super().__init__()
        self.back = back
        self.onOpen = None
        self.onClose = onClose
        self.nugget = nugget

        self.append(
            label.Label(
                terminalio.FONT,
                text=title,
                x=5,
                y=5,
                padding_left=2,
                padding_right=2,
                padding_top=-2,
                color=0x000000,
                background_color=0xFFFFFF,
            )
        )
        self.append(
            label.Label(
                terminalio.FONT,
                text=message,
                x=5,
                y=20,
                padding_left=2,
                padding_right=2,
                padding_top=-2,
                color=0xFFFFFF,
                background_color=0x000000,
                line_spacing=0.8,
            )
        )

    def goBack(self):
        if self.onClose is not None:
            self.onClose()
        self.back.show()

    def show(self):
        self.nugget.setKeybinds(
            {
                "Up": self.goBack,
                "Down": self.goBack,
                "Left": self.goBack,
                "Right": self.goBack,
            }
        )
        self.nugget.switchMenu(self)
