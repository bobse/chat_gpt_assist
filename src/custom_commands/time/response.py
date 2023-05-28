from pydantic import BaseModel
from pydantic.typing import Optional


class Response(BaseModel):
    user_input: str
    action: str
    entity: Optional[str]
