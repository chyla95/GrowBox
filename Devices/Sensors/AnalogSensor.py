from Pins.AnalogPin import AnalogPin
from Utilities.Algorithmes import Algorithmes

class AnalogSensor:

    # Constructors
    def __init__(self, pinNumber:int): 
        self._signalPin = AnalogPin(pinNumber)

    # Properties
    @property
    def SignalPin(self):
        return self._signalPin

    # Methods
    def ReadValue(self) -> int:
        return self.SignalPin.ReadValue()

    def ReadValueInPercent(self, minValue:int, maxValue:int) -> int:
        rawValue = self.ReadValue()   
        return Algorithmes.map(rawValue, minValue, maxValue, 0, 100, keepBoundaries=True)