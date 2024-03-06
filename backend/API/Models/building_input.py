from typing import List, Tuple, Optional

from pydantic import BaseModel


class BuildingInput(BaseModel):
    num_floor: int
    h_opening: Optional[float]
    # (zone_num, elevation)
    zones: Optional[List[Tuple[int, float]]]
    # (zone_num, material_load
    materials: List[Tuple[int, float]]
