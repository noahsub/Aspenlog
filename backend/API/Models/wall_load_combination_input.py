from pydantic import BaseModel


class DimensionsInput(BaseModel):
    uls_wall_type: str
    sls_wall_type: str
