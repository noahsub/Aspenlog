import json
import uuid
import requests
from typing import Optional

from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from numpy import arcsin, sqrt, sin, cos, radians, inf
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
    site_designation: SiteDesignation
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
        self.address = address
        geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace('-', ''))
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location_info = geocode(address, timeout=10)

        # Ensure function is given a valid location
        # TODO: Make custom error for this
        assert location_info is not None

        self.latitude = location_info.latitude
        self.longitude = location_info.longitude

        database = DatabaseConnection(database_name="NBCC-2020")
        # TODO: Change this to READ PrivilegeType
        engine = database.get_engine(privilege=PrivilegeType.ADMIN)
        session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        controller = session()

        # TODO: This can be optimized using PostGIS extension for PostgreSQL
        min_distance = inf
        min_entry = None
        for entry in controller.query(ClimaticData).all():
            # TODO: manually review database to ensure all entries have a valid Latitude and Longitude
            if entry.Latitude is None or entry.Longitude is None:
                continue
            distance = haversine_distance(entry.Latitude, entry.Longitude, self.latitude, self.longitude)
            if distance < min_distance:
                min_distance = distance
                min_entry = entry
            # if this threshold is met, it is close enough and we can stop searching
            if distance < 10:
                break

        self.wind_velocity_pressure = min_entry.HourlyWindPressures_kPa_1_50
        self.snow_load = min_entry.SnowLoad_kPa_1_50_Sr
        self.rain_load = min_entry.SnowLoad_kPa_1_50_Ss

        self.xv = None
        self.xs = None

        match site_designation:
            case site_designation.XV:
                self.site_designation = site_designation.XV
                self.xv = xv
                self.get_seismic_data_xv()
            case site_designation.XS:
                self.site_designation = site_designation.XS
                self.xs = xs
                self.get_seismic_data_xs()

    def get_seismic_data_xv(self):
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n X148: siteDesignationsXv(vs30: {self.xv}, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text)

        self.design_spectral_acceleration_0_2 = data.get('data', {}).get('NBC2020', {}).get('X148', [{}])[0].get(
            'sa0p2')
        self.design_spectral_acceleration_1 = data.get('data', {}).get('NBC2020', {}).get('X148', [{}])[0].get('sa1p0')

    def get_seismic_data_xs(self):
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n XC: siteDesignationsXs(siteClass: C, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text)

        self.design_spectral_acceleration_0_2 = data.get('data', {}).get('NBC2020', {}).get(f'X{self.xs.value}', [{}])[
            0].get('sa0p2')
        self.design_spectral_acceleration_1 = data.get('data', {}).get('NBC2020', {}).get(f'X{self.xs.value}', [{}])[
            0].get('sa1p0')

    def __str__(self):
        return (f"address: {self.address}\n"
                f"latitude: {self.latitude}\n"
                f"longitude: {self.longitude}\n"
                f"site_designation: {self.site_designation}\n"
                f"xv: {self.xv}\n"
                f"xs: {self.xs}\n"
                f"wind_velocity_pressure: {self.wind_velocity_pressure}\n"
                f"snow_load: {self.snow_load}\n"
                f"rain_load: {self.rain_load}\n"
                f"design_spectral_acceleration_0_2: {self.design_spectral_acceleration_0_2}\n"
                f"design_spectral_acceleration_1: {self.design_spectral_acceleration_1}")

    def __dict__(self):
        return {
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "site_designation": self.site_designation,
            "xv": self.xv,
            "xs": self.xs,
            "wind_velocity_pressure": self.wind_velocity_pressure,
            "snow_load": self.snow_load,
            "rain_load": self.rain_load,
            "design_spectral_acceleration_0_2": self.design_spectral_acceleration_0_2,
            "design_spectral_acceleration_1": self.design_spectral_acceleration_1
        }
