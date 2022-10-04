from machine import Pin, I2C, Timer
from Libraries.SSD1306 import SSD1306_I2C

class Display:

    # Constructors
    def __init__(self, displayWidth:int, displayHeight:int, i2cBuss:I2C):
        self._displayWidth = displayWidth
        self._displayHeight = displayHeight
        self._isTurnedOn = None

        self._beingTurnedOnTimer = Timer()
        self._display = SSD1306_I2C(displayWidth, displayHeight, i2cBuss)
        self.Clear()
        self.TurnOff()

    # Properties
    @property
    def DisplayWidth(self):
        return self._displayWidth

    @property
    def DisplayHeight(self):
        return self._displayHeight

    # @property
    # def SclPinNumber(self):
    #     return self._sclPinNumber

    # @property
    # def SdaPinNumber(self):
    #     return self._sdaPinNumber

    @property
    def IsTurnedOn(self):
        return self._isTurnedOn
    @IsTurnedOn.setter
    def IsTurnedOn(self, value):
        self._isTurnedOn = value
    
    # Methods
    def AddText(self, text, xPos, yPos) -> None:     
        self._display.text(text, xPos, yPos)

    def Show(self) -> None:     
        self._display.show()

    def Clear(self) -> None:     
        self._display.fill(0)

    def TurnOff(self) -> None:     
        self._display.poweroff()
        self.IsTurnedOn = False

    def TurnOn(self) -> None:     
        self._display.poweron()
        self.IsTurnedOn = True

    def TurnOnTemporarily(self, time) -> None:     
        self.TurnOn()
        timeInSec = time * 1000
        self._beingTurnedOnTimer.init(mode=Timer.ONE_SHOT, period=timeInSec, callback=lambda s: self.TurnOff())

