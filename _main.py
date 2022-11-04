import time
import uasyncio
from machine import I2C, Pin, Timer
from Devices.Other.Clock import Clock
from Devices.Sensors.SoilMoistureSensor import SoilMoistureSensor
from Devices.Other.Button import Button
from Devices.Other.Display import Display
from Devices.Switchables.GrowLights import GrowLights
from Devices.Switchables.WaterPump import WaterPump
from GrowBox import GrowBox
from Plant import Plant


# Constants
TURN_OFF_DISPALY_DELAY = 10
GROW_BOX_CHECK_EVERY = 10
MAIN_LOOP_DELAY = 1



# General Devices
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=200000)
display = Display(displayWidth=128, displayHeight=32, i2cBuss=i2c)
display.TurnOnTemporarily(TURN_OFF_DISPALY_DELAY)
displayActivationButton = Button(16, Button.Trigger.ON_CLICK, lambda s: display.TurnOnTemporarily(TURN_OFF_DISPALY_DELAY))
clock = Clock(i2c, 0x68)
clock.setTime(year=2022,month=1,day=17,hour=18,minute=59, second=55)

# Plant #1
plant1_SoilMoistureSensor = SoilMoistureSensor(pinNumber=26, minReadableValue=58500, maxReadableValue=25000)
plant1_WaterPump = WaterPump(pinNumber=12)
plant1 = Plant(name="Plant 1", soilMoistureThresholds=(20, 60), wateringDuration_InSec=6, soilMoistureSensor=plant1_SoilMoistureSensor, waterPump=plant1_WaterPump, clock=clock)
plant1.MinDelayBetweenWaterings_InSec = 2 * 60 # Just for safety

# GrowBox #1
growLights = GrowLights(13)
growLights.TurnOff()
growBox1 = GrowBox(name="Main", dayCycle=(19, 20), growLights=growLights, clock=clock)
growBox1.AddPlant(plant1)



# time.sleep(5)
# GrowBox Checking Loop
growBoxCheckingTimer = Timer()
def CheckGrowBoxes(self):
    growBox1.SelfCare()
growBox1.SelfCare()
growBoxCheckingTimer.init(period=(1000 * GROW_BOX_CHECK_EVERY), mode=Timer.PERIODIC, callback=CheckGrowBoxes)

# Loop
while True:
    soilMoisture = round(plant1.GetSoilMoistureInPercent())
    display.Clear()
    display.AddText(f'{clock.Hour if clock.Hour > 10 else "0"+str(clock.Hour)}:{clock.Minute if clock.Minute > 10 else "0"+str(clock.Minute)}', 89, 0)
    display.AddText(f'GrowBox OS', 0, 0)
    display.AddText(f'IN: 12C/34%', 0, 10)
    plantsInfo = ""
    for plant in growBox1.Plants:
        plantsInfo += f'- {plant.GetSoilMoistureInPercent()}%  '
    display.AddText(plantsInfo, 0, 22)
    display.Show()    
    
    print(f'[{clock.Hour}:{clock.Minute}:{clock.Second}]: M: {soilMoisture}% / {plant1.SoilMoistureThresholds[0]}%, - {plant1.NeedsWatering()} / {plant1.CanBeWatered()}')
    time.sleep(MAIN_LOOP_DELAY)






