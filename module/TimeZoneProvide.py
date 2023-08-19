"""
    This module provides timezone recognition
    For now we only hardly support Russian timezones
    It will be changed to recognizing timezones from city names

    Time zones different from Russians will be treated differently (using UTC).
"""

from module.Database import myDatabase
from module.db_query_maker import selectQuery, modifyQuery

import datetime
import pytz


# RUSSIA_TIME_ZONE = {
#     datetime.timedelta(hours=2) : "МСК-1",
#     datetime.timedelta(hours=3) : "МСК",
#     datetime.timedelta(hours=4) : "МСК+1",
#     datetime.timedelta(hours=5) : "МСК+2",
#     datetime.timedelta(hours=6) : "МСК+3",
#     datetime.timedelta(hours=7) : "МСК+4",
#     datetime.timedelta(hours=8) : "МСК+5",
#     datetime.timedelta(hours=9) : "МСК+6",
#     datetime.timedelta(hours=10) : "МСК+7",
#     datetime.timedelta(hours=11) : "МСК+8",
#     datetime.timedelta(hours=12) : "МСК+9",
#     datetime.timedelta(hours=13) : "МСК+10",
#     datetime.timedelta(hours=14) : "МСК+11",
# }


RUSSIA_TIME_ZONE = {
    "+02:00" : "МСК-1",
    "+03:00" : "МСК",
    "+04:00" : "МСК+1",
    "+05:00" : "МСК+2",
    "+06:00" : "МСК+3",
    "+07:00" : "МСК+4",
    "+08:00" : "МСК+5",
    "+09:00" : "МСК+6",
    "+10:00" : "МСК+7",
    "+11:00" : "МСК+8",
    "+12:00" : "МСК+9",
    "+13:00" : "МСК+10",
    "+14:00" : "МСК+11",
}


def stringToOffset(stringOffset):
    """
        This method convents string tz offset to datetime.timedelta
    """

    try:
        sign = 1 if stringOffset[0] == "+" else -1
        if len(stringOffset) != 6 or len(stringOffset.split(":")) != 2 or not stringOffset[0] in ("+", "-"):
            return RuntimeError()
        
        hours, minutes = map(int, stringOffset[1:].split(":"))
        if hours > 23 and minutes > 59:
            raise RuntimeError()
        return datetime.timedelta(hours=sign*hours, minutes=sign*minutes)
    except:
        raise RuntimeError(f"Wrong timeoffset format <{stringOffset}>")


def getUserOffsetString(user_tg_id):
    """
        returns current user's offset from db 
        in format +HH:MM or -HH:MM depending on given offset
    """

    resp = selectQuery("""SELECT timeoffset FROM tzoffset LEFT JOIN user ON tzoffset.user_id=user.id
                            WHERE tg_id=%s;""", [user_tg_id], ["timeoffset"], myDatabase)
    
    if len(resp) != 1:
        # log error
        raise RuntimeError(f"Found not 1 record for user {user_tg_id}")
    
    return resp[0]["timeoffset"]


def conventToUserTZ(given_time, user_tg_id):
    """
        This method applies user's timezone stored in db to given
        datetime object
    """

    # asking db for current user's offset
    offset_string = getUserOffsetString(user_tg_id)
    
    user_offset = datetime.timezone(stringToOffset(offset_string))

    return given_time.astimezone(user_offset)


def dtToBeautifulString(given_time):
    """
        Converts datetime object with offset inside 
        to string format like this 
        "hh:mm dd/mm/yy (UTC+hh:mm)" or "hh:mm dd/mm/yy (МСК+h)" if
        there is appropriate record in RUSSIA_TIME_ZONE variable
    """

    raw_time = given_time.strftime("%H:%M %d/%m/%Y")
    raw_offset = given_time.strftime("%z")
    offset = raw_offset[:3] + ":" + raw_offset[3:]

    # if there is a record in RUSSIA_TIME_ZONE we pass (MCK+h) otherwise (UTC+HH:MM) 
    time_string = raw_time + " " + "(" + (RUSSIA_TIME_ZONE[offset] if offset in RUSSIA_TIME_ZONE else "UTC" + offset) + ")"

    return time_string


def dtToUserTZString(given_time, user_tg_id):
    """
        returns time string built according to given_time datetime object
        and user's time zone
    """

    friendly_time = conventToUserTZ(given_time, user_tg_id)
    friendly_time_string = dtToBeautifulString(friendly_time)

    return friendly_time_string