########################################################################################################################
# building.py
# This file contains classes that represent a building
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import math
from typing import Optional, Dict, List

from backend.Entities.Building.cladding import Cladding
from backend.Entities.Building.dimensions import Dimensions
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Building.material_zone import MaterialZone
from backend.Entities.Building.roof import Roof


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class Building:
    """
    Represents a building
    """

    # Dimensions of the building
    dimensions: Optional[Dimensions]
    # Cladding of the building
    cladding: Optional[Cladding]
    # Roof of the building
    roof: Optional[Roof]
    # Number of height zones in the building
    hz_num: Optional[int]
    # Number of floors in the building
    num_floor: Optional[int]
    # Height of the opening in the building
    h_opening: Optional[float]
    # Height zones of the building
    height_zones: Optional[List[HeightZone]]

    def __init__(self):
        """
        Initializes the Building class
        """
        self.dimensions = None
        self.cladding = None
        self.roof = None
        self.hz_num = None
        self.num_floor = None
        self.h_opening = None
        self.height_zones = None

    def __str__(self):
        """
        String representation of the Building class
        :return:
        """
        # Special formatting for subclasses
        dimensions_str = "\n  " + "\n  ".join(str(self.dimensions).split("\n"))
        cladding_str = "\n  " + "\n  ".join(str(self.cladding).split("\n"))
        roof_str = "\n  " + "\n  ".join(str(self.roof).split("\n"))

        # Special formatting for height zones
        zones_str = "\n"
        for zone in self.height_zones:
            zones_str += f"  height zone {zone.zone_num}\n"
            zone_lst = str(zone).split("\n")
            for i in zone_lst:
                zones_str += f"    {i.lstrip(', ')}\n"
        zones_str = zones_str[:-1]

        # Print each attribute and its value on a new line
        return (
            f"dimensions: {dimensions_str}\n"
            f"cladding: {cladding_str}\n"
            f"roof: {roof_str}\n"
            f"hz_num: {self.hz_num}\n"
            f"num_floor: {self.num_floor}\n"
            f"h_opening: {self.h_opening}\n"
            f"zones: {zones_str}\n"
        )

    def get_height_zone(self, zone_num: int):
        for height_zone in self.height_zones:
            if height_zone.zone_num == zone_num:
                return height_zone
        # TODO: Custom error required
        raise IndexError


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class BuildingBuilderInterface:
    """
    Builder interface for the Building class
    """

    def reset(self):
        pass

    def set_dimensions(self, dimensions: Dimensions):
        pass

    def set_cladding(self, cladding: Cladding):
        pass

    def set_roof(self, roof: Roof):
        pass

    def set_num_floor(self, num_floor: int):
        pass

    def set_h_opening(self, h_opening: float):
        pass

    def get_dimensions(self) -> Dimensions:
        pass

    def get_cladding(self) -> Cladding:
        pass

    def get_roof(self) -> Roof:
        pass

    def get_hz_num(self) -> int:
        pass

    def get_num_floor(self) -> int:
        pass

    def get_h_opening(self) -> float:
        pass

    def get_height_zones(self) -> Dict[HeightZone, Optional[MaterialZone]]:
        pass

    def set_material_load(self, material_load: List[MaterialZone] | float):
        pass


class BuildingDefaultHeightDefaultMaterialBuilder(BuildingBuilderInterface):
    building: Building

    def __init__(self):
        """
        Constructor for the BuildingDefaultHeightDefaultMaterialBuilder class
        """
        # Initialize the builder to its initial state
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.building = Building()

    def set_dimensions(self, dimensions: Dimensions):
        """
        Sets the dimensions attribute of the Building class
        :param dimensions: The dimensions of the building
        :return: None
        """
        self.building.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        """
        Sets the cladding attribute of the Building class
        :param cladding: The cladding of the building
        :return: None
        """
        self.building.cladding = cladding

    def set_roof(self, roof: Roof):
        """
        Sets the roof attribute of the Building class
        :param roof: The roof of the building
        :return: None
        """
        self.building.roof = roof

    def set_num_floor(self, num_floor: int):
        """
        Sets the num_floor attribute of the Building class
        :param num_floor: The number of floors in the building
        :return: None
        """
        self.building.num_floor = num_floor

    def set_h_opening(self, h_opening: float):
        """
        Sets the h_opening attribute of the Building class
        :param h_opening: The height of the opening in the building
        :return: None
        """
        self.building.h_opening = h_opening

    def generate_height_zones(self):
        """
        Generates the height zones of the building
        :return: None
        """
        assert self.building.dimensions is not None

        self.building.height_zones = dict()

        # The default height per height zone is 20 meters
        default_zone_height = 20

        # we take the ceiling of the quotient of the building height divided by the default zone height

        """
        +---------+     ----+
        |         | 6m      |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         +---> 5 height zones
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+     ----+
        """

        self.building.hz_num = math.ceil(
            self.building.dimensions.height / default_zone_height
        )

        # compute the elevation of each height zone
        self.building.height_zones = []
        height_sum = 0
        for i in range(1, self.building.hz_num + 1):
            # the last height zone may be less than the default zone height, in which case we simply take the
            # height of the building
            if i == self.building.hz_num:
                height_sum = self.building.dimensions.height
            else:
                height_sum += 20

            self.building.height_zones.append(
                HeightZone(zone_num=i, elevation=height_sum)
            )

    def set_material_load(self, material_load: List[float] | float):
        """
        Sets the material load of the building
        :param material_load: The material load of the building
        :return: None
        """
        # if the material load is a list, then we set the material load of each height zone
        if isinstance(material_load, list):
            assert len(material_load) == len(self.building.height_zones)
            for i in range(len(self.building.height_zones)):
                self.building.get_height_zone(i + 1).wp = material_load[i]
        # if the material load is a float, then we set the material load of each height zone to the same value
        elif isinstance(material_load, float):
            for height_zone in self.building.height_zones:
                height_zone.wp = material_load

    def get_dimensions(self) -> Dimensions:
        """
        Returns the dimensions attribute of the Building class
        :return: The dimensions of the building
        """
        return self.building.dimensions

    def get_cladding(self) -> Cladding:
        """
        Returns the cladding attribute of the Building class
        :return: The cladding of the building
        """
        return self.building.cladding

    def get_roof(self) -> Roof:
        """
        Returns the roof attribute of the Building class
        :return: The roof of the building
        """
        return self.building.roof

    def get_hz_num(self) -> int:
        """
        Returns the hz_num attribute of the Building class
        :return: The number of height zones in the building
        """
        return self.building.hz_num

    def get_num_floor(self) -> int:
        """
        Returns the num_floor attribute of the Building class
        :return: The number of floors in the building
        """
        return self.building.num_floor

    def get_h_opening(self) -> float:
        """
        Returns the h_opening attribute of the Building class
        :return: The height of the opening in the building
        """
        return self.building.h_opening

    def get_height_zones(self) -> List[HeightZone]:
        """
        Returns the height_zones attribute of the Building class
        :return: The height zones of the building
        """
        return self.building.height_zones

    def get_building(self) -> Building:
        """
        Returns the building object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed building object.
        """
        building = self.building
        self.reset()
        return building


class BuildingCustomHeightDefaultMaterialBuilder(BuildingBuilderInterface):
    building: Building

    def __init__(self):
        """
        Constructor for the BuildingCustomHeightDefaultMaterialBuilder class
        """
        # Initialize the builder to its initial state
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.building = Building()

    def set_dimensions(self, dimensions: Dimensions):
        """
        Sets the dimensions attribute of the Building class
        :param dimensions: The dimensions of the building
        :return: None
        """
        self.building.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        """
        Sets the cladding attribute of the Building class
        :param cladding: The cladding of the building
        :return: None
        """
        self.building.cladding = cladding

    def set_roof(self, roof: Roof):
        """
        Sets the roof attribute of the Building class
        :param roof: The roof of the building
        :return: None
        """
        self.building.roof = roof

    def set_num_floor(self, num_floor: int):
        """
        Sets the num_floor attribute of the Building class
        :param num_floor: The number of floors in the building
        :return: None
        """
        self.building.num_floor = num_floor

    def set_h_opening(self, h_opening: float):
        """
        Sets the h_opening attribute of the Building class
        :param h_opening: The height of the opening in the building
        :return: None
        """
        self.building.h_opening = h_opening

    def generate_height_zones(self, height_zones: List[HeightZone]):
        """
        Generates the height zones of the building
        :param height_zones: The height zones of the building
        :return: None
        """
        assert self.building.dimensions is not None

        self.building.height_zones = dict()

        for height_zone in height_zones:
            self.building.height_zones[height_zone] = None

        highest_height_zone = max(height_zones, key=lambda x: x.elevation)
        assert highest_height_zone.elevation == self.building.dimensions.height

    def get_dimensions(self) -> Dimensions:
        """
        Returns the dimensions attribute of the Building class
        :return: The dimensions of the building
        """
        return self.building.dimensions

    def get_cladding(self) -> Cladding:
        """
        Returns the cladding attribute of the Building class
        :return: The cladding of the building
        """
        return self.building.cladding

    def get_roof(self) -> Roof:
        """
        Returns the roof attribute of the Building class
        :return: The roof of the building
        """
        return self.building.roof

    def get_hz_num(self) -> int:
        """
        Returns the hz_num attribute of the Building class
        :return: The number of height zones in the building
        """
        return self.building.hz_num

    def get_num_floor(self) -> int:
        """
        Returns the num_floor attribute of the Building class
        :return: The number of floors in the building
        """
        return self.building.num_floor

    def get_h_opening(self) -> float:
        """
        Returns the h_opening attribute of the Building class
        :return: The height of the opening in the building
        """
        return self.building.h_opening

    def get_height_zones(self) -> List[HeightZone]:
        """
        Returns the height_zones attribute of the Building class
        :return: The height zones of the building
        """
        return self.building.height_zones

    def get_building(self) -> Building:
        """
        Returns the building object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed building object.
        """
        building = self.building
        self.reset()
        return building

    def set_material_load(self, material_load: List[float] | float):
        """
        Sets the material load of the building
        :param material_load: The material load of the building
        :return: None
        """
        # if the material load is a list, then we set the material load of each height zone
        if isinstance(material_load, list):
            assert len(material_load) == len(self.building.height_zones)
            for i in range(len(self.building.height_zones)):
                self.building.get_height_zone(i + 1).wp = material_load[i]
        # if the material load is a float, then we set the material load of each height zone to the same value
        elif isinstance(material_load, float):
            for height_zone in self.building.height_zones:
                height_zone.wp = material_load


class BuilderDirector:
    @staticmethod
    def construct_building(builder: BuildingBuilderInterface):
        raise NotImplementedError
