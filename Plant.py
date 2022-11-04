from machine import Timer
from Devices.Other.Clock import Clock
from Devices.Sensors.SoilMoistureSensor import SoilMoistureSensor
from Devices.Switchables.WaterPump import WaterPump

class Plant:
    
    def __init__(self, name:str, soilMoistureThresholds:tuple[int, int], wateringDuration_InSec:int, soilMoistureSensor:SoilMoistureSensor, waterPump:WaterPump, clock: Clock):
        self._name = name
        self._soilMoistureThresholds = soilMoistureThresholds       
        self._wateringDuration_InSec = wateringDuration_InSec  
        self._soilMoistureSensor = soilMoistureSensor
        self._waterPump = waterPump
        self._clock = clock

        self._pumpingTimer = Timer()
        self._lastWateringTime:int = 0
        self._wateringsCount:int = 0
        self._minDelayBetweenWaterings_InSec:int = 0

    # Properties
    @property
    def Name(self):
        return self._name

    @property
    def SoilMoistureThresholds(self):
        return self._soilMoistureThresholds

    @property
    def LastWateringTime(self):
        return self._lastWateringTime

    @property
    def WateringsCount(self):
        return self._wateringsCount

    @property
    def MinDelayBetweenWaterings_InSec(self):
        return self._minDelayBetweenWaterings_InSec
    @MinDelayBetweenWaterings_InSec.setter
    def MinDelayBetweenWaterings_InSec(self, value):
        if(value < self.WateringDuration_InSec):
            print(f'Value {value} is too small adn cannot be set as a "MinDelayBetweenWaterings". The value should be >= {self.WateringDuration_InSec}')
        self._minDelayBetweenWaterings_InSec = value
        
    @property
    def WateringDuration_InSec(self):
        return self._wateringDuration_InSec
    @WateringDuration_InSec.setter
    def WateringDuration_InSec(self, value):
        self._wateringDuration_InSec = value

    # Methods
    def GetSoilMoistureInPercent(self) -> int:
        return self._soilMoistureSensor.ReadValueInPercent()
    
    def Water(self) -> None:
        try:
            self._waterPump.TurnOnTemporarily(self.WateringDuration_InSec)
            self._wateringsCount += 1
            self._lastWateringTime = self._clock.TimeStamp
        except RuntimeError as err:
            print(err)

    def StopWatering(self) -> None:
        self._waterPump.TurnOff()

    def NeedsWatering(self) -> bool:
        if(not (self.GetSoilMoistureInPercent() < self.SoilMoistureThresholds[0])):
            return False         
        return True

    def CanBeWatered(self) -> bool:
        if(not self.NeedsWatering()):
            # print(f'{self.Name} doesnt need watering now!')
            return False
        if(not (Clock.TimeDiffInSeconds(self._clock.TimeStamp, self. LastWateringTime) >= self._minDelayBetweenWaterings_InSec)):
            # print(f'{self.Name} was watered recently!')
            return False        
        return True
            