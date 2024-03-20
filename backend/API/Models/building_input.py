########################################################################################################################
# building_input.py
# This file contains the input model for the building object.
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

from pydantic import BaseModel


########################################################################################################################
# MODEL
########################################################################################################################


class BuildingInput(BaseModel):
    """
    The input model for the building object
    """

    # The number of floors in the building
    num_floor: int
    # The mid-height of the building
    h_opening: Optional[float]
    # (zone_num, elevation)
    zones: Optional[List[Tuple[int, float]]]
    # (zone_num, material_load)
    materials: List[Tuple[int, float]]
