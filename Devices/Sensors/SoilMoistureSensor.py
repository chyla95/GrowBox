from Devices.Sensors.AnalogSensor import AnalogSensor

class SoilMoistureSensor(AnalogSensor):
    
    # Constructors
    def __init__(self, pinNumber:int, minReadableValue:int, maxReadableValue:int):
        super().__init__(pinNumber)
        self._minReadableValue = minReadableValue
        self._maxReadableValue = maxReadableValue

    # Properties
    @property
    def MinReadableValue(self):
        return self._minReadableValue

    @property
    def MaxReadableValue(self):
        return self._maxReadableValue

    # Methods
    def ReadValueInPercent(self) -> int:
        return super().ReadValueInPercent(self.MinReadableValue, self.MaxReadableValue)
