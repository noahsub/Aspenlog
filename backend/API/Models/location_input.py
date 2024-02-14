from pydantic import BaseModel


class LocationInput(BaseModel):
    address: str
    site_designation: str
    seismic_value: int | str