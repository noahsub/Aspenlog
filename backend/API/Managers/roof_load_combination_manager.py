########################################################################################################################
# roofs_load_combination_manager.py
# This file manages the roof load combination data for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.roof_load_combination_constants import SLSRoofLoadCombinationTypes, ULSRoofLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import compute_roof_load_combinations


########################################################################################################################
# MANAGER
########################################################################################################################

def process_roof_load_combination_data(building: Building, snow_load_upwind: SnowLoad, snow_load_downwind: SnowLoad,
                                       uls_roof_type: str, sls_roof_type: str):
    """
    Processes the roof load combination data and computes the roof load combinations
    :param building: The building object
    :param snow_load_upwind: The snow load on the upwind side of the building
    :param snow_load_downwind: The snow load on the downwind side of the building
    :param uls_roof_type: The type of ULS roof load combination
    :param sls_roof_type: The type of SLS roof load combination
    :return:
    """
    # Convert the string types to the respective enums
    uls_wall_type = ULSRoofLoadCombinationTypes(uls_roof_type)
    sls_wall_type = SLSRoofLoadCombinationTypes(sls_roof_type)
    # Compute the roof load combinations
    upwind_roof_combination = compute_roof_load_combinations(building, snow_load_upwind, uls_wall_type, sls_wall_type)
    downwind_roof_combination = compute_roof_load_combinations(building, snow_load_downwind, uls_wall_type,
                                                               sls_wall_type)
    # Return the roof load combinations
    return {'upwind': upwind_roof_combination, 'downwind': downwind_roof_combination}
