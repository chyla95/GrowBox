from Devices.Switchables.Adjustable import Adjustable
from Pins.PwmPin import PwmPin
import _thread


class GrowLights(Adjustable):
    # Constructors
    def __init__(self, pinNumber:int, frequency:int = 1000):
        self._maxPower = 100
        super().__init__(pinNumber, frequency)

    # Properties
    @property
    def MaxPower(self):
        return self._maxPower
    @MaxPower.setter
    def MaxPower(self, value):
        self._maxPower = value

    # Methods
    def FadeInAsync(self) -> None:
        try:
            _thread.start_new_thread(self.SetWidthOverTime, (self.MaxPower, 5))
        except RuntimeError as err:
            print(err)
            
    def FadeOutAsync(self) -> None:
        try:
            _thread.start_new_thread(self.SetWidthOverTime, (PwmPin.State.LOW_STATE, 5))
        except RuntimeError as err:
            print(err)