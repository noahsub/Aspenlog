########################################################################################################################
# user.py
# This file contains classes that represent a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################


from typing import Dict, List, Optional

from openpyxl.worksheet.dimensions import Dimension

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Entities.Building.building import Building
from backend.Entities.Building.cladding import Cladding
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Building.roof import Roof
from backend.Entities.Location.location import Location
from backend.Entities.Snow.snow_load import SnowLoad
from backend.Entities.User.profile import Profile

########################################################################################################################
# MAIN CLASS
########################################################################################################################


class User:
    """
    This class is used to store all the information regarding a user
    """

    username: str
    profile: Optional[Profile]
    current_save_file: Optional[int]
    location: Optional[Location]
    dimensions: Optional[Dimension]
    cladding: Optional[Cladding]
    roof: Optional[Roof]
    num_floors: Optional[int]
    mid_height: Optional[float]
    material_load: Optional[Dict[int, float]]
    height_zones: Optional[List[HeightZone]]
    building: Optional[Building]
    importance_category: Optional[ImportanceFactor]
    snow_load: Optional[Dict["str", SnowLoad]]

    def __init__(self, username: str):
        """
        Initializes the User object
        :param username: The username of the user
        """
        self.username = username
        self.profile = None
        self.current_save_file = None
        self.location = None
        self.dimensions = None
        self.cladding = None
        self.roof = None
        self.num_floors = None
        self.mid_height = None
        self.material_load = None
        self.height_zones = None
        self.building = None
        self.importance_category = None
        self.snow_load = None

    def set_profile(self, profile: Profile):
        """
        Sets the profile of the user
        :param profile: The profile of the user
        :return: None
        """
        self.profile = profile

    def set_current_save_file(self, current_save_file: int):
        """
        Sets the current save file of the user
        :param current_save_file: The current save file of the user
        :return: None
        """
        self.current_save_file = current_save_file

    def set_location(self, location: Location):
        """
        Sets the location of the building
        :param location: The location of the building
        :return: None
        """
        self.location = location

    def set_dimensions(self, dimensions: Dimension):
        """
        Sets the dimensions of the user
        :param dimensions: The dimensions of the building
        :return: None
        """
        self.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        """
        Sets the cladding of the building
        :param cladding: The cladding of the building
        :return: None
        """
        self.cladding = cladding

    def set_roof(self, roof: Roof):
        """
        Sets the roof of the building
        :param roof: The roof of the building
        :return: None
        """
        self.roof = roof

    def set_num_floors(self, num_floors: int):
        """
        Sets the number of floors of the building
        :param num_floors: The number of floors of the building
        :return: None
        """
        self.num_floors = num_floors

    def set_mid_height(self, mid_height: float):
        """
        Sets the mid height of the building
        :param mid_height: The mid height of the building
        :return: None
        """
        self.mid_height = mid_height

    def set_material_load(self, material_load: Dict[int, float]):
        """
        Sets the material load of the building
        :param material_load: The material load of the building
        :return: None
        """
        self.material_load = material_load

    def set_height_zones(self, height_zones: List[HeightZone]):
        """
        Sets the height zones of the building
        :param height_zones: The height zones of the building
        :return: None
        """
        self.height_zones = height_zones

    def set_building(self, building: Building):
        """
        Sets the building
        :param building: The building
        :return: None
        """
        self.building = building

    def set_importance_category(self, importance_category: ImportanceFactor):
        """
        Sets the importance category of the building
        :param importance_category: The importance category of the building
        :return: None
        """
        self.importance_category = importance_category

    def set_snow_load(self, snow_load):
        """
        Sets the snow load of the building
        :param snow_load: The snow load of the building
        :return: None
        """
        self.snow_load = snow_load

    def get_username(self):
        """
        Returns the username of the user
        :return: The username of the user
        """
        return self.username

    def get_profile(self):
        """
        Returns the profile of the user
        :return: The profile of the user
        """
        return self.profile

    def get_current_save_file(self):
        """
        Returns the current save file of the user
        :return: The current save file of the user
        """
        return self.current_save_file

    def get_location(self):
        """
        Returns the location of the building
        :return: The location of the building
        """
        return self.location

    def get_dimensions(self):
        """
        Returns the dimensions of the building
        :return: The dimensions of the building
        """
        return self.dimensions

    def get_cladding(self):
        """
        Returns the cladding of the building
        :return: The cladding of the building
        """
        return self.cladding

    def get_roof(self):
        """
        Returns the roof of the building
        :return: The roof of the building
        """
        return self.roof

    def get_num_floors(self):
        """
        Returns the number of floors of the building
        :return: The number of floors of the building
        """
        return self.num_floors

    def get_mid_height(self):
        """
        Returns the mid height of the building
        :return: The mid height of the building
        """
        return self.mid_height

    def get_material_load(self):
        """
        Returns the material load of the building
        :return: The material load of the building
        """
        return self.material_load

    def get_height_zones(self):
        """
        Returns the height zones of the building
        :return: The height zones of the building
        """
        return self.height_zones

    def get_building(self):
        """
        Returns the building
        :return: The building
        """
        return self.building

    def get_importance_category(self):
        """
        Returns the importance category of the building
        :return: The importance category of the building
        """
        return self.importance_category

    def get_snow_load(self):
        """
        Returns the snow load of the building
        :return: The snow load of the building
        """
        return self.snow_load
