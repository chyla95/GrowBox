from Devices.Other.Clock import Clock
from Devices.Switchables.GrowLights import GrowLights
from Plant import Plant

class GrowBox:
    
    def __init__(self, name:str, dayCycle:tuple[int, int], growLights: GrowLights, clock: Clock):
        self._name = name
        self._dayCycle = dayCycle
        self._growLights = growLights
        self._clock = clock
        self._plants: list[Plant] = []

     # Enums
    class TimeOfDay:
        DAY = 0
        NIGHT = 1
        
    # Properties
    @property
    def Name(self):
        return self._name

    @property
    def DayCycle(self):
        return self._dayCycle

    @property
    def Plants(self):
        return self._plants

    # Methods
    def AddPlant(self, plant:Plant) -> None:
        self._plants.append(plant)

    def TurnOnLights(self) -> None:
        self._growLights.FadeInAsync()

    def TurnOffLights(self) -> None:
        self._growLights.FadeOutAsync()

    def GetTimeOfDay(self) -> int:
        if (self._clock.Hour >= self.DayCycle[0] and self._clock.Hour < self.DayCycle[1]):
            return self.TimeOfDay.DAY
        else:
            return self.TimeOfDay.NIGHT

    def SelfCare(self) -> None:  
        isDayTime = (self.GetTimeOfDay() == self.TimeOfDay.DAY) 

        if(isDayTime):
            if(self._growLights.CurentState == GrowLights.State.TURNED_OFF):
                self.TurnOnLights()

        if(not isDayTime):
            if(self._growLights.CurentState == GrowLights.State.TURNED_ON):
                self.TurnOffLights()
            print("Night time - skipping the plant check!")    
           
        for plant in self._plants:
            if(plant.CanBeWatered() and isDayTime):
                plant.Water()

