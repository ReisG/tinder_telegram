'''
    This converts string format time like 
    Thu Aug 03 2023 12:00:00 GMT+0700 (GMT+07:00)
    To datetime object with utc timezone

    Now we assume that user writes time according to his device's time
'''


import datetime
import pytz


def stringTimeConventor(stringTimeFormat):
    month = {"Jun":1, "Feb":2, "Mar":3,
             "Apr":4, "May":5, "Jun":6,
             "Jul":7, "Aug":8, "Sep":9,
             "Oct":10,"Nov":11,"Dec":12}
    
    parsed = stringTimeFormat.split()
    parsedHMS = parsed[4].split(':')

    rawOffset = parsed[5][3:]
    sign = 1 if rawOffset[0] == "+" else -1
    hour = int(rawOffset[1:3])
    minute = int(rawOffset[3:5])

    tzoffset = datetime.timezone(datetime.timedelta(hours=sign*hour, minutes=sign*minute))

    # time according to user's timezone offset
    userstime = datetime.datetime(year=int(parsed[3]),
                                  month=month[parsed[1]],
                                  day=int(parsed[2]),
                                  hour=int(parsedHMS[0]),
                                  minute=int(parsedHMS[1]),
                                  tzinfo=tzoffset
                                  )
    
    # time according to UTC+0
    res = userstime.astimezone(datetime.timezone.utc)

    return res