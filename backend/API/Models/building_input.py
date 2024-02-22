from typing import List, Tuple, Optional
from pydantic import BaseModel


class BuildingInput(BaseModel):
    num_floor: int
    h_opening: float
    # (zone_num, elevation, material_load)
    zones: List[Tuple[int, float, float]]
