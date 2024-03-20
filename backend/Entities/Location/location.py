########################################################################################################################
# location.py
# This file contains classes that represent the location of a building.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import json
import re
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
from database.Entities.canadian_postal_code_data import CanadianPostalCodeData
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


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class Location:
    """
    This class is used to store all the information about a location
    """

    # The address of the location
    address: Optional[str]
    # The latitude and longitude of the location
    latitude: Optional[float]
    longitude: Optional[float]
    # The site designation type
    site_designation: Optional[SiteDesignation]
    # The Vs30 value
    xv: Optional[int]
    # The site class
    xs: Optional[SiteClass]
    # q
    wind_velocity_pressure: Optional[float]
    # Sr
    snow_load: Optional[float]
    # Ss
    rain_load: Optional[float]
    # S_0.2
    design_spectral_acceleration_0_2: Optional[float]
    # S_1
    design_spectral_acceleration_1: Optional[float]

    def __init__(self):
        """
        Constructor for the Location class
        :param address: The address to process
        :param site_designation: The site designation type
        :param xv: The Vs30 value
        :param xs: The site class
        """
        # Set the attributes
        self.address = None
        self.latitude = None
        self.longitude = None
        self.site_designation = None
        self.xv = None
        self.xs = None
        self.wind_velocity_pressure = None
        self.snow_load = None
        self.rain_load = None
        self.design_spectral_acceleration_0_2 = None
        self.design_spectral_acceleration_1 = None

    def find_coordinates(self):
        """
        Finds the latitude and longitude of the location using the address
        :return: None
        """
        assert self.address is not None
        address = self.address

        # extract canadian postal code from address using regex, if it exists
        # also detect postal codes with no space
        postal_code = re.search(r"\b[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d\b", address)
        if postal_code:
            postal_code = postal_code.group(0)
            # capitalize all letters in the postal code
            postal_code = postal_code.upper()
            # ensure that there is a space between the first 3 characters and the last 3 characters
            if len(postal_code) == 6:
                postal_code = postal_code[:3] + " " + postal_code[3:]
            # get the data from the database
            database = DatabaseConnection(database_name="NBCC-2020")
            engine = database.get_engine(privilege=PrivilegeType.ADMIN)
            session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
            controller = session()
            location_info = (
                controller.query(CanadianPostalCodeData)
                .filter_by(postal_code=postal_code)
                .first()
            )
            self.latitude = location_info.latitude
            self.longitude = location_info.longitude
        else:
            geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace("-", ""))
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            location_info = geocode(address, timeout=10)

            # Ensure function is given a valid location
            # TODO: Make custom error for this
            assert location_info is not None

            # Set the latitude and longitude
            self.latitude = location_info.latitude
            self.longitude = location_info.longitude

    def get_seismic_data_xv(self):
        """
        Fetches the seismic data from the NBCC 2020 Seismic Hazard Tool API using the XV site designation
        :return:
        """
        # The url of the API
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        # The payload and headers containing the data we want to use in our POST request
        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n X148: siteDesignationsXv(vs30: {self.xv}, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {"Content-Type": "application/json"}

        # The response received from the POST request
        response = requests.request("POST", url, headers=headers, data=payload)

        # Convert the data to json
        data = json.loads(response.text)

        # Assign the data to the attributes
        self.design_spectral_acceleration_0_2 = (
            data.get("data", {}).get("NBC2020", {}).get("X148", [{}])[0].get("sa0p2")
        )
        self.design_spectral_acceleration_1 = (
            data.get("data", {}).get("NBC2020", {}).get("X148", [{}])[0].get("sa1p0")
        )

    def get_seismic_data_xs(self):
        """
        Fetches the seismic data from the NBCC 2020 Seismic Hazard Tool API using the XS site designation
        :return:
        """
        # The url of the API
        url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"

        # The payload and headers containing the data we want to use in our POST request
        payload = f'{{"query":"query{{\\n NBC2020(latitude: {self.latitude}, longitude: {self.longitude}){{\\n XC: siteDesignationsXs(siteClass: C, poe50: [2.0]){{\\n sa0p2\\n sa1p0\\n }}\\n }}\\n}}","variables":{{}}}}'
        headers = {"Content-Type": "application/json"}

        # The response received from the POST request
        response = requests.request("POST", url, headers=headers, data=payload)

        # Convert the data to json
        data = json.loads(response.text)

        # example data
        # {'data': {'NBC2020': {'XC': [{'sa0p2': 0.658, 'sa1p0': 0.209}]}}}

        # Assign the data to the attributes
        self.design_spectral_acceleration_0_2 = data["data"]["NBC2020"]["XC"][0][
            "sa0p2"
        ]
        self.design_spectral_acceleration_1 = data["data"]["NBC2020"]["XC"][0]["sa1p0"]

    def get_climatic_data(self):
        """
        Fetches the climatic data from the database
        :return: None
        """
        # Connect to the database
        database = DatabaseConnection(database_name="NBCC-2020")
        engine = database.get_engine(privilege=PrivilegeType.ADMIN)
        session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        controller = session()

        # Get the climatic data of the closest location in the database
        # Future: This can be optimized using PostGIS extension for PostgreSQL
        min_distance = inf
        min_entry = None
        # Iterate through all entries in the database (small enough that we can do this until we optimize code)
        for entry in controller.query(ClimaticData).all():
            # TODO: manually review database to ensure all entries have a valid Latitude and Longitude
            if entry.Latitude is None or entry.Longitude is None:
                continue
            distance = haversine_distance(
                entry.Latitude, entry.Longitude, self.latitude, self.longitude
            )
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

    def __str__(self):
        """
        String representation of the Location class
        :return:
        """
        # Print each attribute and its value on a new line
        return (
            f"address: {self.address}\n"
            f"latitude: {self.latitude}\n"
            f"longitude: {self.longitude}\n"
            f"site_designation: {self.site_designation}\n"
            f"xv: {self.xv}\n"
            f"xs: {self.xs}\n"
            f"wind_velocity_pressure: {self.wind_velocity_pressure}\n"
            f"snow_load: {self.snow_load}\n"
            f"rain_load: {self.rain_load}\n"
            f"design_spectral_acceleration_0_2: {self.design_spectral_acceleration_0_2}\n"
            f"design_spectral_acceleration_1: {self.design_spectral_acceleration_1}"
        )


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class LocationBuilderInterface:
    """
    Builder interface for the Location class
    """

    def reset(self):
        pass

    def set_address(self, address: str):
        pass

    def set_coordinates(self):
        pass

    def set_seismic_data(self):
        pass

    def set_climatic_data(self):
        pass

    def get_address(self) -> str:
        pass

    def get_latitude(self) -> float:
        pass

    def get_longitude(self) -> float:
        pass

    def get_site_designation(self) -> SiteDesignation:
        pass

    def get_xv(self) -> int:
        pass

    def get_xs(self) -> SiteClass:
        pass

    def get_wind_velocity_pressure(self) -> float:
        pass

    def get_snow_load(self) -> float:
        pass

    def get_rain_load(self) -> float:
        pass

    def get_design_spectral_acceleration_0_2(self) -> float:
        pass

    def get_design_spectral_acceleration_1(self) -> float:
        pass


class LocationXvBuilder:
    """
    Concrete builder class for the Location class
    """

    location: Location

    def __init__(self):
        """
        Constructor for the LocationBuilder class
        """
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.location = Location()

    def set_address(self, address: str):
        """
        Sets the address of the location
        :param address: The address of the location
        :return: None
        """
        self.location.address = address

    def set_coordinates(self):
        """
        Finds the latitude and longitude of the location using the address
        :return: None
        """
        assert self.location.address is not None
        self.location.find_coordinates()

    def set_seismic_data(self, xv: int):
        """
        Sets the seismic data of the location using the XV site designation
        :param xv: The Vs30 value
        :return: None
        """
        self.location.site_designation = SiteDesignation.XV
        self.location.xv = xv
        self.location.get_seismic_data_xv()

    def set_climatic_data(self):
        """
        Fetches the climatic data from the database
        :return: None
        """
        assert self.location.address is not None
        assert self.location.latitude is not None
        assert self.location.longitude is not None
        self.location.get_climatic_data()

    def get_address(self) -> str:
        """
        Returns the address of the location
        :return: The address of the location
        """
        return self.location.address

    def get_latitude(self) -> float:
        """
        Returns the latitude of the location
        :return: The latitude of the location
        """
        return self.location.latitude

    def get_longitude(self) -> float:
        """
        Returns the longitude of the location
        :return: The longitude of the location
        """
        return self.location.longitude

    def get_site_designation(self) -> SiteDesignation:
        """
        Returns the site designation of the location
        :return: The site designation of the location
        """
        return self.location.site_designation

    def get_xv(self) -> int:
        """
        Returns the Vs30 value of the location
        :return: The Vs30 value of the location
        """
        return self.location.xv

    def get_wind_velocity_pressure(self) -> float:
        """
        Returns the wind velocity pressure of the location
        :return: The wind velocity pressure of the location
        """
        return self.location.wind_velocity_pressure

    def get_snow_load(self) -> float:
        """
        Returns the snow load of the location
        :return: The snow load of the location
        """
        return self.location.snow_load

    def get_rain_load(self) -> float:
        """
        Returns the rain load of the location
        :return: The rain load of the location
        """
        return self.location.rain_load

    def get_design_spectral_acceleration_0_2(self) -> float:
        """
        Returns the design spectral acceleration at 0.2 seconds of the location
        :return: The design spectral acceleration at 0.2 seconds of the location
        """
        return self.location.design_spectral_acceleration_0_2

    def get_design_spectral_acceleration_1(self) -> float:
        """
        Returns the design spectral acceleration at 1 second of the location
        :return: The design spectral acceleration at 1 second of the location
        """
        return self.location.design_spectral_acceleration_1

    def get_location(self) -> Location:
        """
        Returns the location object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed location object.
        """
        location = self.location
        self.reset()
        return location


class LocationXsBuilder:
    """
    Concrete builder class for the Location class
    """

    location: Location

    def __init__(self):
        """
        Constructor for the LocationBuilder class
        """
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.location = Location()

    def set_address(self, address: str):
        """
        Sets the address of the location
        :param address: The address of the location
        :return: None
        """
        self.location.address = address

    def set_coordinates(self):
        """
        Finds the latitude and longitude of the location using the address
        :return: None
        """
        assert self.location.address is not None
        self.location.find_coordinates()

    def set_seismic_data(self, xs: SiteClass):
        """
        The seismic data of the location using the XS site designation
        :param xs: The site class
        :return: None
        """
        self.location.site_designation = SiteDesignation.XS
        self.location.xs = xs
        self.location.get_seismic_data_xs()

    def set_climatic_data(self):
        """
        Fetches the climatic data from the database
        :return: None
        """
        assert self.location.address is not None
        assert self.location.latitude is not None
        assert self.location.longitude is not None
        self.location.get_climatic_data()

    def get_address(self) -> str:
        """
        Returns the address of the location
        :return: The address of the location
        """
        return self.location.address

    def get_latitude(self) -> float:
        """
        Returns the latitude of the location
        :return: The latitude of the location
        """
        return self.location.latitude

    def get_longitude(self) -> float:
        """
        Returns the longitude of the location
        :return: The longitude of the location
        """
        return self.location.longitude

    def get_site_designation(self) -> SiteDesignation:
        """
        Returns the site designation of the location
        :return: The site designation of the location
        """
        return self.location.site_designation

    def get_xs(self) -> SiteClass:
        """
        Returns the site class of the location
        :return: The site class of the location
        """
        return self.location.xs

    def get_wind_velocity_pressure(self) -> float:
        """
        Returns the wind velocity pressure of the location
        :return: The wind velocity pressure of the location
        """
        return self.location.wind_velocity_pressure

    def get_snow_load(self) -> float:
        """
        Returns the snow load of the location
        :return: The snow load of the location
        """
        return self.location.snow_load

    def get_rain_load(self) -> float:
        """
        Returns the rain load of the location
        :return: The rain load of the location
        """
        return self.location.rain_load

    def get_design_spectral_acceleration_0_2(self) -> float:
        """
        Returns the design spectral acceleration at 0.2 seconds of the location
        :return: The design spectral acceleration at 0.2 seconds of the location
        """
        return self.location.design_spectral_acceleration_0_2

    def get_design_spectral_acceleration_1(self) -> float:
        """
        Returns the design spectral acceleration at 1 second of the location
        :return: The design spectral acceleration at 1 second of the location
        """
        return self.location.design_spectral_acceleration_1

    def get_location(self) -> Location:
        """
        Returns the location object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed location object.
        """
        location = self.location
        self.reset()
        return location
