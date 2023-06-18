from typing import Literal
from pydantic import BaseModel


class Response(BaseModel):
    user_input: str
    action: Literal["power", "volume", "app", "control", "input"]
    entity: str
