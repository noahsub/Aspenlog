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
from typing import Optional
from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.materials import Materials
from backend.Entities.Building.cladding import Cladding
from backend.Entities.Building.dimensions import Dimensions
from backend.Entities.Building.height_zone import HeightZone
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
    height_zones: Optional[list[HeightZone]]
    # Dead load for the building
    wp: Optional[float]

    def __init__(self):
        self.dimensions = None
        self.cladding = None
        self.roof = None
        self.hz_num = None
        self.num_floor = None
        self.h_opening = None
        self.height_zones = None
        self.wp = None

    def compute_height_zones(self, selection: DefaultSelections, height_zones: list[HeightZone] = None):
        """
        Computes the height zones of the building
        :param selection: Determines weather default or custom values are used
        :param height_zones: The list of height zones to use if custom values are used
        :return: None
        """
        # Differentiate between default and custom selection
        match selection:
            # If default, compute the height zones based on the height of the building
            case selection.DEFAULT:
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

                self.hz_num = math.ceil(self.dimensions.height / default_zone_height)

                # compute the elevation of each height zone
                self.height_zones = []
                height_sum = 0
                for i in range(1, self.hz_num + 1):
                    # the last height zone may be less than the default zone height, in which case we simply take the
                    # height of the building
                    if i == self.hz_num:
                        height_sum = self.dimensions.height
                    else:
                        height_sum += 20
                    self.height_zones.append(HeightZone(zone_num=i, elevation=height_sum))
            # If custom, use the provided height zones
            case selection.CUSTOM:
                self.height_zones = height_zones

    def compute_dead_load(self, selection: DefaultSelections, wp: float = None):
        """
        Computes the dead load of the building
        :param selection: Determines weather default or custom values are used
        :param wp: The dead load to use if custom values are used
        :return: None
        """
        # Differentiate between default and custom selection
        match selection:
            # If default, use the provided dead load
            case selection.DEFAULT:
                self.wp = wp
            # If custom, compute the dead load based on the material percentages and elevation of each height zone
            case selection.CUSTOM:
                # ensure that all height zones have a valid material mapping
                assert all([height_zone.wp_materials is not None and
                            len(height_zone.wp_materials) <= len(Materials.get_materials_list())
                            for height_zone in self.height_zones])
                # compute dead load as weighted average based on material percentages and elevation
                self.wp = 0
                products = []
                material_sum = 0
                for height_zone in self.height_zones:
                    product = sum(x * height_zone.elevation for x in height_zone.wp_materials.values())
                    products.append(product)
                    material_sum += sum(height_zone.wp_materials.values())
                self.wp = sum(products) / material_sum

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
        height_zones_str = '\n'
        for height_zone in self.height_zones:
            height_zones_str += f"  height zone {height_zone.zone_num}\n"
            height_zone_lst = str(height_zone).split('\n')
            for i in height_zone_lst:
                height_zones_str += f"    {i.lstrip(', ')}\n"
        height_zones_str = height_zones_str[:-1]

        # Print each attribute and its value on a new line
        return (f"dimensions: {dimensions_str}\n"
                f"cladding: {cladding_str}\n"
                f"roof: {roof_str}\n"
                f"hz_num: {self.hz_num}\n"
                f"num_floor: {self.num_floor}\n"
                f"h_opening: {self.h_opening}\n"
                f"height_zones: {height_zones_str}\n"
                f"wp: {self.wp}")


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

    def set_hz_num(self, hz_num: int):
        pass

    def set_num_floor(self, num_floor: int):
        pass

    def set_h_opening(self, h_opening: float):
        pass

    def set_height_zones(self, height_zones: list[HeightZone]):
        pass

    def set_wp(self, wp: float):
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

    def get_height_zones(self) -> list[HeightZone]:
        pass

    def get_wp(self) -> float:
        pass


class BuildingBuilder(BuildingBuilderInterface):
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

    def set_hz_num(self, hz_num: int):
        self.building.hz_num = hz_num

    def set_num_floor(self, num_floor: int):
        self.building.num_floor = num_floor

    def set_h_opening(self, h_opening: float):
        self.building.h_opening = h_opening

    def set_height_zones(self, height_zones: list[HeightZone]):
        self.building.height_zones = height_zones

    def set_wp(self, wp: float):
        self.building.wp = wp

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

    def get_height_zones(self) -> list[HeightZone]:
        return self.building.height_zones

    def get_wp(self) -> float:
        return self.building.wp

    def get_building(self) -> Building:
        building = self.building
        self.reset()
        return building


class BuilderDirector:
    @staticmethod
    def construct_building(builder: BuildingBuilderInterface):
        raise NotImplementedError