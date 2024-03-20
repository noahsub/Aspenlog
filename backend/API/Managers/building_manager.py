########################################################################################################################
# building_manager.py
# This file manages the building data and processes it to create a building object for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from typing import List, Tuple, Optional

from backend.API.Managers.user_data_manager import (
    get_user_dimensions,
    get_user_cladding,
    get_user_roof,
)
from backend.Entities.Building.building import (
    BuildingDefaultHeightDefaultMaterialBuilder,
    BuildingCustomHeightDefaultMaterialBuilder,
)
from backend.Entities.Building.height_zone import HeightZone

########################################################################################################################
# MANAGER
########################################################################################################################


def process_building_data(
    num_floor: int,
    h_opening: Optional[float],
    zones: Optional[List[Tuple[int, float]]],
    materials: List[Tuple[int, float]],
    username,
):
    """
    Processes the building data and creates a building object
    :param num_floor: The number of floors in the building
    :param h_opening: The mid-height opening in the building
    :param zones: The height zones in the building
    :param materials: The material load in the building
    :param username: The username of the user
    :return: A building object
    """
    # If the mid-height opening is not provided, set it to 0
    if h_opening is None:
        h_opening = 0
    # Get the user's dimensions, cladding, and roof
    dimensions = get_user_dimensions(username)
    cladding = get_user_cladding(username)
    roof = get_user_roof(username)
    # If the zones are provided, create a height zone object for each height zone
    if zones is not None:
        height_zones = [HeightZone(zone_num=x[0], elevation=x[1]) for x in zones]
    # If the zones are not provided, set the height zones to None
    else:
        height_zones = None
    # Get the material load for each height zone
    material_load = [x[1] for x in materials]

    # Case default height zones and simple material load
    if height_zones is None and isinstance(material_load, (list, float)):
        building_builder = BuildingDefaultHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones()
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    # Case custom height zones and simple material load
    elif height_zones is not None and isinstance(material_load, (list, float)):
        building_builder = BuildingCustomHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones(height_zones)
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    # This should never happen
    else:
        raise NotImplementedError
