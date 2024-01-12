########################################################################################################################
# building.py
# This file contains classes that represent a building and its components
# Classes include:
#   - Dimensions: represents the dimensions of a building
#   - Cladding: represents the cladding of a building
#   - Roof: represents the roof of a building
#   - HeightZone: represents a height zone of a building
#   - Building: represents a building
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import math
from typing import Optional, Dict
from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.materials import Materials


########################################################################################################################
# SUBCLASSES
########################################################################################################################


class HeightZone:
    """
    Represents a height zone of a building
    """
    # Number of the height zone
    zone_num: int
    # Elevation of the height zone
    elevation: float
    # Material percentages for the height zone
    wp_materials: Optional[Dict[Materials, float]]

    def __init__(self, zone_num: int, elevation: float):
        """
        Constructor for HeightZone class
        :param zone_num: Number of the height zone
        :param elevation: Elevation of the height zone
        """
        # Set the zone number and elevation
        self.zone_num = zone_num
        self.elevation = elevation
        # Initialize to None for string representation purposes
        self.wp_materials = None

    def __str__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n,"
                f"wp_materials: {self.wp_materials}")


########################################################################################################################
# MAIN CLASS
########################################################################################################################

class Building:
    """
    Represents a building
    """
    # Dimensions of the building
    dimensions: Dimensions
    # Cladding of the building
    cladding: Cladding
    # Roof of the building
    roof: Roof
    # Number of height zones in the building
    hz_num: Optional[int]
    # Number of floors in the building
    num_floor: int
    # Height of the opening in the building
    h_opening: float
    # Height zones of the building
    height_zones: Optional[list[HeightZone]]
    # Dead load for the building
    wp: Optional[float]

    def __init__(self, dimensions: Dimensions, cladding: Cladding, roof: Roof, num_floor: int, h_opening: float):
        """
        Constructor for Building class
        :param dimensions: Dimensions of the building
        :param cladding: Cladding of the building
        :param roof: Roof of the building
        :param num_floor: Number of floors in the building
        :param h_opening: Dominant opening of the building
        """
        # Set the attributes
        self.dimensions = dimensions
        self.cladding = cladding
        self.roof = roof
        self.num_floor = num_floor
        self.h_opening = h_opening
        # Initialize to None for string representation purposes
        self.hz_num = None
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

# Sample Usage
# if __name__ == '__main__':
#     dimensions = Dimensions(height=86, width=50)
#     cladding = Cladding(2, 2)
#     roof = Roof(50, 50, 45)
#     building = Building(dimensions, cladding, roof, 0)
#     print([str(x) for x in building.height_zones])
