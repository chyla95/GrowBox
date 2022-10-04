import utime

class TimeStamp:
    def __init__(self, year:int, month:int, day:int, hour:int, minute:int, second:int):
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second

    # Properties
    @property
    def Year(self):
        return self._year
    @property
    def Month(self):
        return self._month
    @property
    def Day(self):
        return self._day
    @property
    def Hour(self):
        return self._hour
    @property
    def Minute(self):
        return self._minute
    @property
    def Second(self):
        return self._second
    @property
    def WeekDay(self):
        return self._getWeekDay(self.Year, self.Month, self.Day)
    @property
    def TimeStamp(self):
        return utime.mktime((self.Year, self.Month, self.Day, self.Hour, self.Minute, self.Second, self.WeekDay, 0))

    # Methods
    @staticmethod
    def _getWeekDay(year:int, month:int, day:int) -> int:
        offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        afterFeb = 1
        if month > 2: afterFeb = 0
        aux = year - 1700 - afterFeb
        # dayOfWeek for 1700/1/1 = 5, Friday
        dayOfWeek  = 5
        # partial sum of days betweem current date and 1700/1/1
        dayOfWeek += (aux + afterFeb) * 365                  
        # leap year correction    
        dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
        # sum monthly and day offsets
        dayOfWeek += offset[month - 1] + (day - 1)               
        dayOfWeek %= 7
        return int(dayOfWeek)



class _BaseRTC:
    _DATETIME_REGISTER = None
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address

    def _register(self, register, buffer=None):
        if buffer is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, buffer)

    def _flag(self, register, mask, value=None):
        data = self._register(register)
        if value is None:
            return bool(data & mask)
        if value:
            data |= mask
        else:
            data &= ~mask
        self._register(register, bytearray((data,)))

    def _bcd2bin(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)

    def _bin2bcd(self,value):
        return (value or 0) + 6 * ((value or 0) // 10)

    def setTime(self, year:int, month:int, day:int, hour:int, minute:int, second:int) -> None:        
        buffer = bytearray(7)
        buffer[0] = self._bin2bcd(second)
        buffer[1] = self._bin2bcd(minute)
        buffer[2] = self._bin2bcd(hour)
        buffer[3] = self._bin2bcd(TimeStamp._getWeekDay(year, month, day))
        buffer[4] = self._bin2bcd(day)
        buffer[5] = self._bin2bcd(month)
        buffer[6] = self._bin2bcd(year - 2000)
        self._register(self._DATETIME_REGISTER, buffer)

    def _getTime(self) -> TimeStamp:
        buffer = self.i2c.readfrom_mem(self.address, self._DATETIME_REGISTER, 7)
        second=self._bcd2bin(buffer[0])
        minute=self._bcd2bin(buffer[1])
        hour=self._bcd2bin(buffer[2])
        #weekday=self._bcd2bin(buffer[3])
        day=self._bcd2bin(buffer[4])
        month=self._bcd2bin(buffer[5])
        year=self._bcd2bin(buffer[6]) + 2000
        return TimeStamp(year, month, day, hour, minute, second)



class DS1307(_BaseRTC):
    _NVRAM_REGISTER = 0x08
    _DATETIME_REGISTER = 0x00
    _SQUARE_WAVE_REGISTER = 0x07

    def stop(self, value=None):
        return self._flag(0x00, 0b10000000, value)

    def memory(self, address, buffer=None):
        if buffer is not None and address + len(buffer) > 56:
            raise ValueError("address out of range")
        return self._register(self._NVRAM_REGISTER + address, buffer)



# class DS3231(_BaseRTC):
#     _CONTROL_REGISTER = 0x0e
#     _STATUS_REGISTER = 0x0f
#     _DATETIME_REGISTER = 0x00
#     _ALARM_REGISTERS = (0x08, 0x0b)
#     _SQUARE_WAVE_REGISTER = 0x0e

#     def lost_power(self):
#         return self._flag(self._STATUS_REGISTER, 0b10000000)

#     def alarm(self, value=None, alarm=0):
#         return self._flag(self._STATUS_REGISTER,
#                           0b00000011 & (1 << alarm), value)

#     def interrupt(self, alarm=0):
#         return self._flag(self._CONTROL_REGISTER,
#                           0b00000100 | (1 << alarm), 1)

#     def no_interrupt(self):
#         return self._flag(self._CONTROL_REGISTER, 0b00000011, 0)

#     def stop(self, value=None):
#         return self._flag(self._CONTROL_REGISTER, 0b10000000, value)

#     def datetime(self, datetime=None):
#         if datetime is not None:
#             status = self._register(self._STATUS_REGISTER) & 0b01111111
#             self._register(self._STATUS_REGISTER, bytearray((status,)))
#         return super().datetime(datetime)

#     def alarm_time(self, datetime=None, alarm=0):
#         if datetime is None:
#             buffer = self.i2c.readfrom_mem(self.address,
#                                            self._ALARM_REGISTERS[alarm], 3)
#             day = None
#             weekday = None
#             second = None
#             if buffer[2] & 0b10000000:
#                 pass
#             elif buffer[2] & 0b01000000:
#                 day = _bcd2bin(buffer[2] & 0x3f)
#             else:
#                 weekday = _bcd2bin(buffer[2] & 0x3f)
#             minute = (_bcd2bin(buffer[0] & 0x7f)
#                       if not buffer[0] & 0x80 else None)
#             hour = (_bcd2bin(buffer[1] & 0x7f)
#                     if not buffer[1] & 0x80 else None)
#             if alarm == 0:
#                 # handle seconds
#                 buffer = self.i2c.readfrom_mem(
#                     self.address, self._ALARM_REGISTERS[alarm] - 1, 1)
#                 second = (_bcd2bin(buffer[0] & 0x7f)
#                           if not buffer[0] & 0x80 else None)
#             return datetime_tuple(
#                 day=day,
#                 weekday=weekday,
#                 hour=hour,
#                 minute=minute,
#                 second=second,
#             )
#         datetime = datetime_tuple(*datetime)
#         buffer = bytearray(3)
#         buffer[0] = (_bin2bcd(datetime.minute)
#                      if datetime.minute is not None else 0x80)
#         buffer[1] = (_bin2bcd(datetime.hour)
#                      if datetime.hour is not None else 0x80)
#         if datetime.day is not None:
#             if datetime.weekday is not None:
#                 raise ValueError("can't specify both day and weekday")
#             buffer[2] = _bin2bcd(datetime.day)
#         elif datetime.weekday is not None:
#             buffer[2] = _bin2bcd(datetime.weekday) | 0b01000000
#         else:
#             buffer[2] = 0x80
#         self._register(self._ALARM_REGISTERS[alarm], buffer)
#         if alarm == 0:
#             # handle seconds
#             buffer = bytearray([_bin2bcd(datetime.second)
#                                 if datetime.second is not None else 0x80])
#             self._register(self._ALARM_REGISTERS[alarm] - 1, buffer)



# class PCF8523(_BaseRTC):
#     _CONTROL1_REGISTER = 0x00
#     _CONTROL2_REGISTER = 0x01
#     _CONTROL3_REGISTER = 0x02
#     _DATETIME_REGISTER = 0x03
#     _ALARM_REGISTER = 0x0a
#     _SQUARE_WAVE_REGISTER = 0x0f
#     _SWAP_DAY_WEEKDAY = True

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.init()

#     def init(self):
#         # Enable battery switchover and low-battery detection.
#         self._flag(self._CONTROL3_REGISTER, 0b11100000, False)

#     def reset(self):
#         self._flag(self._CONTROL1_REGISTER, 0x58, True)
#         self.init()

#     def lost_power(self, value=None):
#         return self._flag(self._CONTROL3_REGISTER, 0b00010000, value)

#     def stop(self, value=None):
#         return self._flag(self._CONTROL1_REGISTER, 0b00010000, value)

#     def battery_low(self):
#         return self._flag(self._CONTROL3_REGISTER, 0b00000100)

#     def alarm(self, value=None):
#         return self._flag(self._CONTROL2_REGISTER, 0b00001000, value)

#     def datetime(self, datetime=None):
#         if datetime is not None:
#             self.lost_power(False) # clear the battery switchover flag
#         return super().datetime(datetime)

#     def alarm_time(self, datetime=None):
#         if datetime is None:
#             buffer = self.i2c.readfrom_mem(self.address,
#                                            self._ALARM_REGISTER, 4)
#             return datetime_tuple(
#                 weekday=_bcd2bin(buffer[3] &
#                                  0x7f) if not buffer[3] & 0x80 else None,
#                 day=_bcd2bin(buffer[2] &
#                              0x7f) if not buffer[2] & 0x80 else None,
#                 hour=_bcd2bin(buffer[1] &
#                               0x7f) if not buffer[1] & 0x80 else None,
#                 minute=_bcd2bin(buffer[0] &
#                                 0x7f) if not buffer[0] & 0x80 else None,
#             )
#         datetime = datetime_tuple(*datetime)
#         buffer = bytearray(4)
#         buffer[0] = (_bin2bcd(datetime.minute)
#                      if datetime.minute is not None else 0x80)
#         buffer[1] = (_bin2bcd(datetime.hour)
#                      if datetime.hour is not None else 0x80)
#         buffer[2] = (_bin2bcd(datetime.day)
#                      if datetime.day is not None else 0x80)
#         buffer[3] = (_bin2bcd(datetime.weekday) | 0b01000000
#                      if datetime.weekday is not None else 0x80)
#         self._register(self._ALARM_REGISTER, buffer)