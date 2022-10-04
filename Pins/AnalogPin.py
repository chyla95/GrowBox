from machine import ADC

class AnalogPin(ADC):

    # Constructors
    def __init__(self, pinNumber:int):
        self._pinNumber = pinNumber
        super().__init__(pinNumber)

    # Properties
    @property
    def PinNumber(self):
        return self._pinNumber

    # Methods
    def ReadValue(self) -> int:     
        return self.read_u16()