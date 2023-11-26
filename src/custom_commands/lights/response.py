from enum import Enum, auto
from pydantic import BaseModel


class LightStateEnum(str, Enum):
    ON = "on"
    OFF = "off"


class Response(BaseModel):
    user_input: str
    action: LightStateEnum
    entity: str
