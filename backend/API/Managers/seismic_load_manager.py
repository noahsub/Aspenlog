########################################################################################################################
# set_seismic_load_data.py
# This file manages the creation of a seismic load object for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from copy import deepcopy

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Seismic.seismic_factor import SeismicFactorBuilder
from backend.Entities.Seismic.seismic_load import SeismicLoadBuilder
from backend.algorithms.seismic_load_algorithms import get_seismic_factor_values, get_height_factor, \
    get_horizontal_force_factor, get_specified_lateral_earthquake_force


########################################################################################################################
# MANAGER
########################################################################################################################

def process_seismic_load_data(building: Building, location: Location, importance_category: ImportanceFactor, ar: float, rp: float, cp: float):
    """
    Processes the seismic load data and creates a seismic load object
    :param building: The building object
    :param location: The location object
    :param importance_category: The importance category
    :param ar: The force amplification factor
    :param rp: The response modification factor
    :param cp: The component factor
    :return: None
    """
    # Create a seismic factor builder object
    seismic_factor_builder = SeismicFactorBuilder()
    # Set the seismic factor values
    get_seismic_factor_values(seismic_factor_builder, ar, rp, cp)
    # For each height zone in the building, calculate the seismic load
    for height_zone in building.height_zones:
        # Create a copy of the seismic factor builder object
        zone_seismic_factor_builder = deepcopy(seismic_factor_builder)
        # Create a seismic load builder object
        seismic_load_builder = SeismicLoadBuilder()
        # Set the height factor
        get_height_factor(seismic_load_builder, building, height_zone.zone_num)
        # Set the horizontal force factor
        get_horizontal_force_factor(zone_seismic_factor_builder, seismic_load_builder)
        # Set the specified lateral earthquake force
        get_specified_lateral_earthquake_force(seismic_load_builder, building, height_zone.zone_num, location, importance_category)
        # Get the seismic load
        seismic_load = seismic_load_builder.get_seismic_load()
        # Set the seismic load in the height zone
        height_zone.seismic_load = seismic_load
