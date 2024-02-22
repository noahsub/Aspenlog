from typing import Optional
from pydantic import BaseModel


class DimensionsInput(BaseModel):
    width: float
    height: Optional[float]
    eave_height: Optional[float]
    ridge_height: Optional[float]
