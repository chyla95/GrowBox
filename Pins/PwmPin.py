from machine import Pin, PWM

class PwmPin(PWM):

    # Constructors
    def __init__(self, pinNumber:int, frequency:int = 1000):
        self._pinNumber = pinNumber
        super().__init__(Pin(pinNumber))
        self.freq(frequency)
        self._width = PwmPin.State.LOW_STATE

     # Enums
    class State:
        LOW_STATE = 0
        HIGH_STATE = 65536

    # Properties
    @property
    def PinNumber(self):
        return self._pinNumber

    @property
    def Width(self):
        return self._width

    # Methods
    def SetFrequency(self, value) -> None:     
        if (value < 0):
            value = 0
        self.freq(value)
        
    def SetWidth(self, value) -> None:     
        if (value < self.State.LOW_STATE):
            value = self.State.LOW_STATE
        elif(value > self.State.HIGH_STATE):
            value = self.State.HIGH_STATE
        self._width = value
        self.duty_u16(value)