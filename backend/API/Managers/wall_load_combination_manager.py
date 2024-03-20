########################################################################################################################
# walls_load_combination_manager.py
# This file manages the wall load combination data for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.wall_load_combination_constants import (
    ULSWallLoadCombinationTypes,
    SLSWallLoadCombinationTypes,
)
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import (
    compute_wall_load_combinations,
)


########################################################################################################################
# MANAGER
########################################################################################################################


def process_wall_load_combination_data(
    building: Building, snow_load: SnowLoad, uls_wall_type: str, sls_wall_type: str
):
    """
    Processes the wall load combination data and computes the wall load combinations
    :param building: The building object
    :param snow_load: The snow load object
    :param uls_wall_type: The type of ULS wall load combination
    :param sls_wall_type: The type of SLS wall load combination
    :return: A dataframe containing the wall load combinations
    """
    uls_wall_type = ULSWallLoadCombinationTypes(uls_wall_type)
    sls_wall_type = SLSWallLoadCombinationTypes(sls_wall_type)
    return compute_wall_load_combinations(
        building, snow_load, uls_wall_type, sls_wall_type
    )
