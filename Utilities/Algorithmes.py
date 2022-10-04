class Algorithmes:

    @staticmethod
    def map(value:int, fromMin:int, fromMax:int, ToMin:int, toMax:int, keepBoundaries:bool = False) -> int:
        # Figure out how 'wide' each range is
        leftSpan = fromMax - fromMin
        rightSpan = toMax - ToMin
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - fromMin) / float(leftSpan)
        # Convert the 0-1 range into a value in the right range and fix boundaries and 
        result = ToMin + (valueScaled * rightSpan)
        if(keepBoundaries):
            if (result < ToMin):
                result = ToMin
            if(result > toMax):
                result = toMax
        # Convert the 0-1 range into a value in the right range.
        return int(result)

