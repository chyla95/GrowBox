from machine import Pin

class DigitalPin(Pin):
    
    # Constructors
    def __init__(self, pinNumber:int, pinMode:int, pinPullMode:int | None = None):
        self._pinNumber = pinNumber
        self._pinMode = pinMode
        self._pinPullMode = pinPullMode
        
        if (pinPullMode == None):
            super().__init__(pinNumber, pinMode)            
        else:
            super().__init__(pinNumber, pinMode, pinPullMode)   

     # Enums
    class State:
        LOW_STATE = 0
        HIGH_STATE = 1

    # Properties 
    @property
    def PinNumber(self):
        return self._pinNumber

    @property
    def PinMode(self):
        return self._pinMode

    @property
    def PinPullMode(self):
        return self._pinPullMode

    # Methods
    def ReadState(self) -> int | None:
        return self.value() # as self.State

    def SetState(self, state:int) -> None:
        if(self.PinMode == Pin.OUT):
            self.value(state) # as self
        else:
            raise RuntimeError(f'Pin {self.PinNumber} is in a "INPUT" mode. Setting state is not possible!')

         