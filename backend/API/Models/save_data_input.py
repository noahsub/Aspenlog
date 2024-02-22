from typing import Optional

from pydantic import BaseModel


class SaveDataInput(BaseModel):
    json_data: str
    id: Optional[int]

