########################################################################################################################
# building.py
# This file contains classes that represent a building
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
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
# SUBCLASSES
########################################################################################################################


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
        dimensions_str = '\n  ' + '\n  '.join(str(self.dimensions).split('\n'))
        cladding_str = '\n  ' + '\n  '.join(str(self.cladding).split('\n'))
        roof_str = '\n  ' + '\n  '.join(str(self.roof).split('\n'))

        # Special formatting for height zones
        zones_str = '\n'
        for zone in self.height_zones:
            zones_str += f"  height zone {zone.zone_num}\n"
            zone_lst = str(zone).split('\n')
            for i in zone_lst:
                zones_str += f"    {i.lstrip(', ')}\n"
        zones_str = zones_str[:-1]

        # Print each attribute and its value on a new line
        return (f"dimensions: {dimensions_str}\n"
                f"cladding: {cladding_str}\n"
                f"roof: {roof_str}\n"
                f"hz_num: {self.hz_num}\n"
                f"num_floor: {self.num_floor}\n"
                f"h_opening: {self.h_opening}\n"
                f"zones: {zones_str}\n")

    def get_height_zone(self, zone_num: int):
        for height_zone in self.height_zones:
            if height_zone.zone_num == zone_num:
                return height_zone
        # TODO: Custom error required
        raise IndexError


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
        self.reset()

    def reset(self):
        self.building = Building()

    def set_dimensions(self, dimensions: Dimensions):
        self.building.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        self.building.cladding = cladding

    def set_roof(self, roof: Roof):
        self.building.roof = roof

    def set_num_floor(self, num_floor: int):
        self.building.num_floor = num_floor

    def set_h_opening(self, h_opening: float):
        self.building.h_opening = h_opening

    def generate_height_zones(self):
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

        self.building.hz_num = math.ceil(self.building.dimensions.height / default_zone_height)

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

            self.building.height_zones.append(HeightZone(zone_num=i, elevation=height_sum))

    def set_material_load(self, material_load: List[float] | float):
        if isinstance(material_load, list):
            assert len(material_load) == len(self.building.height_zones)
            for i in range(len(self.building.height_zones)):
                self.building.get_height_zone(i + 1).wp = material_load[i]

        elif isinstance(material_load, float):
            for height_zone in self.building.height_zones:
                height_zone.wp = material_load

    def get_dimensions(self) -> Dimensions:
        return self.building.dimensions

    def get_cladding(self) -> Cladding:
        return self.building.cladding

    def get_roof(self) -> Roof:
        return self.building.roof

    def get_hz_num(self) -> int:
        return self.building.hz_num

    def get_num_floor(self) -> int:
        return self.building.num_floor

    def get_h_opening(self) -> float:
        return self.building.h_opening

    def get_height_zones(self) -> List[HeightZone]:
        return self.building.height_zones

    def get_building(self) -> Building:
        building = self.building
        self.reset()
        return building


class BuildingCustomHeightDefaultMaterialBuilder(BuildingBuilderInterface):
    building: Building

    def __init__(self):
        self.reset()

    def reset(self):
        self.building = Building()

    def set_dimensions(self, dimensions: Dimensions):
        self.building.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        self.building.cladding = cladding

    def set_roof(self, roof: Roof):
        self.building.roof = roof

    def set_num_floor(self, num_floor: int):
        self.building.num_floor = num_floor

    def set_h_opening(self, h_opening: float):
        self.building.h_opening = h_opening

    def generate_height_zones(self, height_zones: List[HeightZone]):
        assert self.building.dimensions is not None

        self.building.height_zones = dict()

        for height_zone in height_zones:
            self.building.height_zones[height_zone] = None

        highest_height_zone = max(height_zones, key=lambda x: x.elevation)
        assert highest_height_zone.elevation <= self.building.dimensions.height

    def get_dimensions(self) -> Dimensions:
        return self.building.dimensions

    def get_cladding(self) -> Cladding:
        return self.building.cladding

    def get_roof(self) -> Roof:
        return self.building.roof

    def get_hz_num(self) -> int:
        return self.building.hz_num

    def get_num_floor(self) -> int:
        return self.building.num_floor

    def get_h_opening(self) -> float:
        return self.building.h_opening

    def get_height_zones(self) -> List[HeightZone]:
        return self.building.height_zones

    def get_building(self) -> Building:
        building = self.building
        self.reset()
        return building

    def set_material_load(self, material_load: List[float] | float):
        if isinstance(material_load, list):
            assert len(material_load) == len(self.building.height_zones)
            for i in range(len(self.building.height_zones)):
                self.building.get_height_zone(i + 1).wp = material_load[i]

        elif isinstance(material_load, float):
            for height_zone in self.building.height_zones:
                height_zone.wp = material_load


class BuilderDirector:
    @staticmethod
    def construct_building(builder: BuildingBuilderInterface):
        raise NotImplementedError
