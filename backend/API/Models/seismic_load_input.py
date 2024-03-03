from pydantic import BaseModel


class SeismicLoadInput(BaseModel):
    ar: float
    rp: float
    cp: float
