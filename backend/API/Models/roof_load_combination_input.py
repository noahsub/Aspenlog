from pydantic import BaseModel


class RoofLoadCombinationInput(BaseModel):
    uls_roof_type: str
    sls_roof_type: str