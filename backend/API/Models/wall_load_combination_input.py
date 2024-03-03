from pydantic import BaseModel


class WallLoadCombinationInput(BaseModel):
    uls_wall_type: str
    sls_wall_type: str
