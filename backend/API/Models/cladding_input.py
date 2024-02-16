from pydantic import BaseModel


class CladdingInput(BaseModel):
    c_top: float
    c_bot: float
