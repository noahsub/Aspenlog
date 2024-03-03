from pydantic import BaseModel


class DimensionsInput(BaseModel):
    uls_roof_type: str
    sls_roof_type: str