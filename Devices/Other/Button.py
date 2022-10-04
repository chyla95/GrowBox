from machine import Pin
from Devices.Sensors.DigitalSensor import DigitalSensor

class Button(DigitalSensor):      

    # Constructors
    def __init__(self, pinNumber:int, trigger:int, callBack):
        self._pinNumber = pinNumber         
        super().__init__(pinNumber, Pin.IN, Pin.PULL_DOWN)       

        if(trigger == self.Trigger.ON_CLICK):            
            self.SignalPin.irq(callBack, Pin.IRQ_RISING)
        elif (trigger == self.Trigger.ON_RELEASE):
            self.SignalPin.irq(callBack, Pin.IRQ_FALLING)

    # Enums
    class Trigger:
        ON_CLICK = 0
        ON_RELEASE = 1

    # Properties

    # Methods

    