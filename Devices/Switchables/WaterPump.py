from Devices.Switchables.Switchable import Switchable

class WaterPump(Switchable):
    def __init__(self, pinNumber:int):
        super().__init__(pinNumber)

