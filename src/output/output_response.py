from pydantic import BaseModel
from pydantic.typing import Optional


class OutputResponse(BaseModel):
    raw_text: Optional[str]
    formated_text: Optional[str]
    success: bool
