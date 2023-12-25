import math
import uuid
from typing import Optional

from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from numpy import arcsin, sqrt, sin, cos, radians
from sqlalchemy.orm import sessionmaker

from backend.Constants.location_constants import EARTH_RADIUS
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from database.Constants.connection_constants import PrivilegeType
from database.Entities.climatic_data import ClimaticData
from database.Entities.database_connection import DatabaseConnection


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = radians([lat1, lon1, lat2, lon2])
    a = (sin((lat2 - lat1) / 2)) ** 2
    b = cos(lat1)
    c = cos(lat2)
    d = (sin((lon2 - lon1) / 2)) ** 2
    distance = 2 * EARTH_RADIUS * arcsin(sqrt(a + b * c * d))
    return distance


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

    def __init__(self, address: str, site_designation: SiteDesignation, xv: int = None, xs: SiteClass = None):
        # geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace('-', ''))
        # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        # location_info = geocode(address, timeout=10)
        #
        # self.latitude = location_info.latitude
        # self.longitude = location_info.longitude

        database = DatabaseConnection(database_name="NBCC-2020")
        # TODO: Change this to READ PrivilegeType
        engine = database.get_engine(privilege=PrivilegeType.ADMIN)
        session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        controller = session()

        # for entry in controller.query(ClimaticData).all():
