from pydantic import BaseModel


class RoofInput(BaseModel):
    w_roof: float
    l_roof: float
    slope: float
    uniform_dead_load: float
