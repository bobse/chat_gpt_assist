from pydantic import BaseModel


class Response(BaseModel):
    user_input: str
    action: bool
    entity: str
