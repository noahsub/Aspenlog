########################################################################################################################
# seismic_load_algorithms.py
# This file contains the algorithms for calculating seismic loads
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.importance_factor_constants import SeismicImportanceFactor
from backend.Entities.building import Building
from backend.Entities.location import Location
from backend.Entities.seismic import SeismicLoad
from backend.Entities.snow import SnowLoad


########################################################################################################################
# SEISMIC LOAD ALGORITHMS
########################################################################################################################

def get_seismic_factor_values(seismic_load: SeismicLoad, ar: float = 1, rp: float = 2.5, cp: float = 1):
    """
    This function sets the seismic factor values
    :param seismic_load: A SeismicLoad object, responsible for storing the seismic load information
    :param ar: Element or component force amplification factor
    :param rp: Element of component response modification factor
    :param cp: Element of component factor
    :return: None
    """
    # if ar parameter is present, override default value
    if ar:
        seismic_load.factor.ar = ar
    # if rp parameter is present, override default value
    if rp:
        seismic_load.factor.rp = rp
    # if cp parameter is present, override default value
    if cp:
        seismic_load.factor.cp = cp


def get_floor_mapping(building: Building):
    """
    This function maps the floor number to the appropriate height zone number
    :param building: A Building object, responsible for storing the building information
    :return: A mapping of the floor number to the height zone number
    """
    # TODO: Needs to be optimized
    # TODO: Bug here. num_floor is a string when execution of this function is reached
    building.num_floor = int(int(building.num_floor))
    # Get the height of the floors
    floor_height = building.dimensions.height / building.num_floor
    # Create a dictionary used to map the floor number to the height zone number
    floor_mapping = {}
    for floor in range(1, building.num_floor + 1, 1):
        for zone in building.height_zones:
            # If the floor elevation is less than or equal to the zone elevation, then the floor is in that zone
            if floor * floor_height <= zone.elevation:
                # assign the floor number to the zone number in the mapping
                floor_mapping[floor] = zone.zone_num
                # break out of the loop, and move to the next floor
                break
    # return the mapping
    return floor_mapping


def get_height_factor(seismic_load: SeismicLoad, building: Building, floor: int):
    """
    This function calculates the height factor
    :param seismic_load: A SeismicLoad object, responsible for storing the seismic load information
    :param building: A Building object, responsible for storing the building information
    :param floor: The floor number to be used in the computation
    :return: None
    """
    # Ax=1+2*hx_n/H
    seismic_load.ax = 1 + 2 * floor / building.dimensions.height


def get_horizontal_force_factor(seismic_load: SeismicLoad):
    """
    This function calculates the horizontal force factor for the part or portion of the building
    :param seismic_load: A SeismicLoad object, responsible for storing the seismic load information
    :return: None
    """
    # Sp = Cp * Ar * Ax / Rp
    # Range of Sp: [0.7, 4]
    seismic_load.sp = seismic_load.factor.cp * seismic_load.factor.ar * seismic_load.ax / seismic_load.factor.rp


def get_specified_lateral_earthquake_force(seismic_load: SeismicLoad, snow_load: SnowLoad, building: Building,location: Location, seismic_importance_factor: SeismicImportanceFactor):
    """
    This function calculates the specified lateral earthquake force
    :param seismic_load: A SeismicLoad object, responsible for storing the seismic load information
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param building: A Building object, responsible for storing the building information
    :param location: A Location object, responsible for storing the location information
    :param seismic_importance_factor: The seismic importance factor to be used in the computation
    :return: None
    """
    # Vp=0.3*S_0.2*Ie*Sp*Wp
    seismic_load.vp = 0.3 * location.design_spectral_acceleration_0_2 * seismic_importance_factor.value * seismic_load.sp * building.wp
    # Vp_snow=0.3*S_0.2*Ie*Wp_snow where Wp_snow=S+Wp
    seismic_load.vp_snow = 0.3 * location.design_spectral_acceleration_0_2 * seismic_importance_factor.value * (snow_load.s + building.wp)
