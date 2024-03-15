from pydantic import BaseModel


class SimpleModelInput(BaseModel):
    total_elevation: float
    roof_angle: float
