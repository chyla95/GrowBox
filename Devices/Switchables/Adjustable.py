import time
from Pins.PwmPin import PwmPin
from Utilities.Algorithmes import Algorithmes
import uasyncio

class Adjustable:
    # Constructors
    def __init__(self, pinNumber:int, frequency:int = 1000):
        self._signalPin = PwmPin(pinNumber, frequency)
        self._state = Adjustable.State.TURNED_OFF

    # Enums
    class State:
        TURNED_OFF = 0
        TURNED_ON = 1
        BUSY = 2

    # Properties
    @property
    def SignalPin(self):
        return self._signalPin
    
    @property
    def Width(self):
        return self.SignalPin.Width

    @property
    def CurentState(self):
        return self._state
        
    # Methods
    def SetWidth(self, value) -> None:     
        self.SignalPin.SetWidth(value)
        self._state = Adjustable.State.TURNED_ON if (self.Width > 0) else Adjustable.State.TURNED_OFF

    def TurnOn(self) -> None:
        self.SetWidth(PwmPin.State.HIGH_STATE)

    def TurnOff(self) -> None:
        self.SetWidth(PwmPin.State.LOW_STATE)

    def SetWidthInPercent(self, value) -> None:     
        minValue = PwmPin.State.LOW_STATE
        maxValue = PwmPin.State.HIGH_STATE
        self.SetWidth(Algorithmes.map(value, 0, 100, minValue, maxValue, keepBoundaries=True))
        # self.SignalPin.duty_u16(Algorithmes.map(value, 0, 100, minValue, maxValue, keepBoundaries=True))

    def SetWidthOverTime(self, value, duration) -> None:   
        if(self.CurentState == Adjustable.State.BUSY):
            raise RuntimeError('The "Adjustable" component is Busy...')
        self._state = Adjustable.State.BUSY
        duration = duration * 1000
        minValue = PwmPin.State.LOW_STATE
        maxValue = PwmPin.State.HIGH_STATE 
        targetRawPower = Algorithmes.map(value, 0, 100, minValue, maxValue, keepBoundaries=True)
        iterationDurationOffset = self.Width if self.Width > PwmPin.State.LOW_STATE else PwmPin.State.LOW_STATE + 1
        
        if(self.Width > targetRawPower):
            iterationDuration = (duration / iterationDurationOffset) /10
            while(self.Width > targetRawPower):
                self.SetWidth(self.Width - 100)
                time.sleep(iterationDuration)
            self.SetWidth(targetRawPower)
            #self.TurnOff()
        else:
            iterationDuration = (duration / targetRawPower) /10
            while(self.Width < targetRawPower):
                self.SetWidth(self.Width + 100)
                time.sleep(iterationDuration ) 
            self.SetWidth(targetRawPower)
            #self.TurnOn()