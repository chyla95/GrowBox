from Pins.DigitalPin import DigitalPin

class DigitalSensor:

    # Constructors
    def __init__(self, pinNumber:int, pinMode:int, pinPullMode:int = None):
        if(pinPullMode == None):
            self._signalPin = DigitalPin(pinNumber, pinMode)
        else:
            self._signalPin = DigitalPin(pinNumber, pinMode, pinPullMode)        

    # Properties
    @property
    def SignalPin(self):
        return self._signalPin
        
    # Methods
    def ReadState(self) -> int:
        return self.SignalPin.ReadState()