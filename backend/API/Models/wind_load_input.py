from typing import Optional, List

from pydantic import BaseModel


class WindLoadInput(BaseModel):
    ct: List[float]
    exposure_factor: List[str]
    manual_ce_cei: List[Optional[float]]
    internal_pressure_category: List[str]
