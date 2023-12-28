########################################################################################################################
# location.py
# This file contains the Location class, which is used to store all the information about a location
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

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

########################################################################################################################
# HELPER FUNCTIONS
########################################################################################################################


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on the earth's surface using the haversine formula
    :param lat1: The latitude of the first point
    :param lon1: The longitude of the first point
    :param lat2: The latitude of the second point
    :param lon2: The longitude of the second point
    :return: The distance between the two points in km
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = radians([lat1, lon1, lat2, lon2])
    # Haversine formula
    # Reference: https://en.wikipedia.org/wiki/Haversine_formula
    a = (sin((lat2 - lat1) / 2)) ** 2
    b = cos(lat1)
    c = cos(lat2)
    d = (sin((lon2 - lon1) / 2)) ** 2
    distance = 2 * EARTH_RADIUS * arcsin(sqrt(a + b * c * d))
    # Return distance in km
    return distance


class Location:
    """
    This class is used to store all the information about a location
    """
    # The address of the location
    address: str
    # The latitude and longitude of the location
    latitude: float
    longitude: float
    # The site designation type
    site_designation: SiteDesignation
    # The Vs30 value
    xv: Optional[int]
    # The site class
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
        """
        Constructor for the Location class
        :param address: The address to process
        :param site_designation: The site designation type
        :param xv: The Vs30 value
        :param xs: The site class
        """
        # Set the address
        self.address = address
        # Get geographic information about the address
        geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace('-', ''))
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location_info = geocode(address, timeout=10)

        # Ensure function is given a valid location
        # TODO: Make custom error for this
        assert location_info is not None

        # Set the latitude and longitude
        self.latitude = location_info.latitude
        self.longitude = location_info.longitude

        # Connect to the database
        database = DatabaseConnection(database_name="NBCC-2020")
        # TODO: Change this to READ PrivilegeType
        engine = database.get_engine(privilege=PrivilegeType.ADMIN)
        session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        controller = session()

        # Get the climatic data of the closest location in the database
        # TODO: This can be optimized using PostGIS extension for PostgreSQL
        min_distance = inf
        min_entry = None
        # Iterate through all entries in the database (small enough that we can do this until we optimize code)
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

        # Set the climatic attributes
        self.wind_velocity_pressure = min_entry.HourlyWindPressures_kPa_1_50
        self.snow_load = min_entry.SnowLoad_kPa_1_50_Sr
        self.rain_load = min_entry.SnowLoad_kPa_1_50_Ss

        # Set to None for string representation purposes
        self.xv = None
        self.xs = None

        # Differentiate between site designation types
        match site_designation:
            # If the site designation is XV
            case site_designation.XV:
                # Set the xv value
                self.site_designation = site_designation.XV
                self.xv = xv
                # Fetch data from the NBCC 2020 Seismic Hazard Tool API
                self.get_seismic_data_xv()
            # If the site designation is XS
            case site_designation.XS:
                # Set the xs value
                self.site_designation = site_designation.XS
                self.xs = xs
                # Fetch data from the NBCC 2020 Seismic Hazard Tool API
                self.get_seismic_data_xs()

    def get_seismic_data_xv(self):
        """
        Fetches the seismic data from the NBCC 2020 Seismic Hazard Tool API using the XV site designation
        :return:
        """
        # The url of the API
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        # The payload and headers containing the data we want to use in our POST request
        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n X148: siteDesignationsXv(vs30: {self.xv}, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {
            'Content-Type': 'application/json'
        }

        # The response received from the POST request
        response = requests.request("POST", url, headers=headers, data=payload)

        # Convert the data to json
        data = json.loads(response.text)

        # Assign the data to the attributes
        self.design_spectral_acceleration_0_2 = data.get('data', {}).get('NBC2020', {}).get('X148', [{}])[0].get('sa0p2')
        self.design_spectral_acceleration_1 = data.get('data', {}).get('NBC2020', {}).get('X148', [{}])[0].get('sa1p0')

    def get_seismic_data_xs(self):
        """
        Fetches the seismic data from the NBCC 2020 Seismic Hazard Tool API using the XS site designation
        :return:
        """
        # The url of the API
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        # The payload and headers containing the data we want to use in our POST request
        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n XC: siteDesignationsXs(siteClass: C, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {
            'Content-Type': 'application/json'
        }

        # The response received from the POST request
        response = requests.request("POST", url, headers=headers, data=payload)

        # Convert the data to json
        data = json.loads(response.text)

        # Assign the data to the attributes
        self.design_spectral_acceleration_0_2 = data.get('data', {}).get('NBC2020', {}).get(f'X{self.xs.value}', [{}])[0].get('sa0p2')
        self.design_spectral_acceleration_1 = data.get('data', {}).get('NBC2020', {}).get(f'X{self.xs.value}', [{}])[0].get('sa1p0')

    def __str__(self):
        """
        String representation of the Location class
        :return:
        """
        # Print each attribute and its value on a new line
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
