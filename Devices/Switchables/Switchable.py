from machine import Pin, Timer
from Pins.DigitalPin import DigitalPin

class Switchable:
        # Constructors
    def __init__(self, pinNumber:int):
        self._signalPin = DigitalPin(pinNumber, Pin.OUT)

        self._turnOnTemporarilyTimer = Timer()
        self._state = Switchable.State.TURNED_OFF

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
    def CurentState(self):
        return self._state
        
    # Methods
    def TurnOn(self) -> None:
        self.SignalPin.SetState(DigitalPin.State.HIGH_STATE)
        self._state = Switchable.State.TURNED_ON

    def TurnOff(self) -> None:
        self.SignalPin.SetState(DigitalPin.State.LOW_STATE)
        self._state = Switchable.State.TURNED_OFF

    def TurnOnTemporarily(self, duration) -> None:
        if(self._state == Switchable.State.BUSY):
            raise RuntimeError('The "Switchable" component is Busy...')       

        self.SignalPin.SetState(DigitalPin.State.HIGH_STATE)
        self._state = Switchable.State.BUSY

        self._turnOnTemporarilyTimer.init(mode=Timer.ONE_SHOT, period=(1000*duration), callback=lambda s: self.TurnOff())