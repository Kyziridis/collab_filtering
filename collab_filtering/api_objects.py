from enum import Enum
from datetime import datetime
from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, validator, ValidationError, constr


class EventTypeModel(Enum):
    waypoint = 'waypoint'  # denoting a 30 seconds watched interval
    streamstart = 'streamstart'  # denoting the start of a stream
    streamstop = 'streamstop'  # denoting a client-initiated stop of stream
    # denoting the end of the media item is reached, should occur once for each user-item combination
    streamend = 'streamend'


class RequestInputData(BaseModel):
    EventId: str
    UserId: Union[int, str]
    MediaId: Union[int, str]
    Timestamp: int
    DateTime: datetime
    EventType: EventTypeModel

    @validator('EventId', pre=True)
    def check_eventid(cls, v):
        if len(v) != 64:
            raise HTTPException(
                status_code=422,
                detail=[{'loc': ['body', 'EventId'],
                         'msg': 'value is not containing 64 chars', 'type': 'type_error.str'}])
        return v

    @validator('UserId')
    def check_userid(cls, UserId):
        if isinstance(UserId, str)\
                and UserId.startswith("\'"):
            UserId = int(UserId.strip('\''))
        elif isinstance(UserId, int):
            pass
        else:
            raise HTTPException(
                status_code=422,
                detail=[{'loc': ['body', 'UserId'],
                         'msg': 'value is correct', 'type': 'type_error.str'}])
        return UserId

    @validator('MediaId')
    def check_mediaid(cls, MediaId):
        if isinstance(MediaId, str)\
                and MediaId.startswith("\'"):
            MediaId = int(MediaId.strip('\''))
        elif isinstance(MediaId, int):
            pass
        else:
            raise HTTPException(
                status_code=422,
                detail=[{'loc': ['body', 'MediaId'],
                         'msg': 'value is correct', 'type': 'type_error.str'}])
        return MediaId
