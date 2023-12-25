from typing import Optional

from backend.Constants.seismic_constants import SiteClass, SiteDesignation


class Location:
    address: str
    latitude: float
    longitude: float
    xv: Optional[int]
    xs: Optional[SiteClass]
    # q
    wind_velocity_pressure: float
    # Sr
    snow_load: float
    # Ss
    rain_load: float
    # S_0.2
    design_spectral_acceleration_0_2: float
    # S_1
    design_spectral_acceleration_1: float

    # def __init__(self, address: str, site_designation: SiteDesignation, xv: int = None, xs: SiteClass = None):
    #




