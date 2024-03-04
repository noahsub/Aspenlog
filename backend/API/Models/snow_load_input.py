from pydantic import BaseModel


class SnowLoadInput(BaseModel):
    exposure_factor_selection: str
    roof_type: str
