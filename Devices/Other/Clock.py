from Libraries.RtcLib import DS1307, TimeStamp

class Clock(DS1307):
    def __init__(self, i2c, address=0x68):
        super().__init__(i2c, address)

    # Properties
    @property
    def Year(self):
        return self._getTime().Year
    @property
    def Month(self):
        return self._getTime().Month
    @property
    def Day(self):
        return self._getTime().Day
    @property
    def Hour(self):
        return self._getTime().Hour
    @property
    def Minute(self):
        return self._getTime().Minute
    @property
    def Second(self):
        return self._getTime().Second
    @property
    def WeekDay(self):
        return self._getTime().WeekDay
    @property
    def TimeStamp(self):
        return self._getTime().TimeStamp

    @staticmethod
    def TimeDiffInSeconds(timeStampBase:int, timeStampOff:int) -> int:
        return abs(timeStampBase - timeStampOff)   

    @staticmethod
    def TimeDiffInMinutes(timeStampBase:int, timeStampOff:int) -> float:
        return Clock.TimeDiffInSeconds(timeStampBase, timeStampOff) / 60

    @staticmethod
    def TimeDiffInHours(timeStampBase:int, timeStampOff:int) -> float:
        return Clock.TimeDiffInSeconds(timeStampBase, timeStampOff) / 60 / 60  

#err value timestamp = 946684880