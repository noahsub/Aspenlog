########################################################################################################################
# seismic_load_algorithms.py
# This file contains the algorithms for calculating seismic loads
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Constants.load_constants import LoadTypes
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Seismic.seismic_factor import SeismicFactorBuilder
from backend.Entities.Seismic.seismic_load import SeismicLoadBuilder


########################################################################################################################
# SEISMIC LOAD ALGORITHMS
########################################################################################################################


def get_seismic_factor_values(
    seismic_factor_builder: SeismicFactorBuilder,
    ar: float = 1,
    rp: float = 2.5,
    cp: float = 1,
):
    """
    This function sets the seismic factor values
    :param seismic_factor_builder:
    :param ar: Element or component force amplification factor
    :param rp: Element of component response modification factor
    :param cp: Element of component factor
    :return: None
    """
    # if ar parameter is present, override default value
    seismic_factor_builder.set_ar(ar)
    # if rp parameter is present, override default value
    seismic_factor_builder.set_rp(rp)
    # if cp parameter is present, override default value
    seismic_factor_builder.set_cp(cp)


def get_floor_mapping(building: Building):
    """
    This function maps the floor number to the appropriate height zone number
    :param building: A Building object, responsible for storing the building information
    :return: A mapping of the floor number to the height zone number
    """
    building.num_floor = int(int(building.num_floor))
    # Get the height of the floors
    floor_height = building.dimensions.height / building.num_floor
    # Create a dictionary used to map the floor number to the height zone number
    floor_mapping = {}
    for floor in range(1, building.num_floor + 1, 1):
        for height_zone in building.height_zones:
            # If the floor elevation is less than or equal to the zone elevation, then the floor is in that zone
            if floor * floor_height <= height_zone.elevation:
                # assign the floor number to the zone number in the mapping
                floor_mapping[floor] = height_zone.zone_num
                # break out of the loop, and move to the next floor
                break
    # return the mapping
    return floor_mapping


def get_height_factor(
    seismic_load_builder: SeismicLoadBuilder, building: Building, zone_num: int
):
    """
    This function calculates the height factor
    :param zone_num: The numerical identifier for the height zone
    :param seismic_load_builder: A SeismicLoadBuilder object, responsible for building the seismic load information
    :param building: A Building object, responsible for storing the building information
    :return: None
    """
    height_zone = building.get_height_zone(zone_num)
    # Ax=1+2*H_hz_num/H
    seismic_load_builder.set_ax(
        1 + 2 * (height_zone.elevation / building.dimensions.height)
    )


def get_horizontal_force_factor(
    seismic_factor_builder: SeismicFactorBuilder,
    seismic_load_builder: SeismicLoadBuilder,
):
    """
    This function calculates the horizontal force factor for the part or portion of the building
    :return: None
    """
    # Sp = Cp * Ar * Ax / Rp
    # Range of Sp: [0.7, 4]
    seismic_load_builder.set_sp(
        seismic_factor_builder.get_cp()
        * seismic_factor_builder.get_ar()
        * seismic_load_builder.get_ax()
        / seismic_factor_builder.get_rp()
    )
    seismic_factor = seismic_factor_builder.get_seismic_factor()
    seismic_load_builder.set_factor(seismic_factor)


def get_specified_lateral_earthquake_force(
    seismic_load_builder: SeismicLoadBuilder,
    building: Building,
    height_zone_num: int,
    location: Location,
    importance_factor: ImportanceFactor,
):
    """
    This function calculates the specified lateral earthquake force
    :param importance_factor: The selected importance factor
    :param height_zone_num: The numerical identifier for the height zone
    :param seismic_load_builder: A SeismicLoadBuilder object, responsible for building the seismic load information
    :param building: A Building object, responsible for storing the building information
    :param location: A Location object, responsible for storing the location information
    :return: None
    """
    seismic_importance_factor = importance_factor.get_importance_factor_uls(
        LoadTypes.SEISMIC
    )
    # Vp=0.3*S_0.2*Ie*Sp*Wp
    seismic_load_builder.set_vp(
        0.3
        * location.design_spectral_acceleration_0_2
        * seismic_importance_factor
        * seismic_load_builder.get_sp()
        * building.get_height_zone(height_zone_num).wp
    )
