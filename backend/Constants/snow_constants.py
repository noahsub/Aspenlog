########################################################################################################################
# snow_constants.py
# This file contains the constants and enums pertaining to snow
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from enum import Enum

########################################################################################################################
# CONSTANTS
########################################################################################################################

# The snow accumulation factor
ACCUMULATION_FACTOR = 1


########################################################################################################################
# ENUMS
########################################################################################################################

class RoofType(Enum):
    """
    Enum for the roof types
    """
    UNOBSTRUCTED_SLIPPERY_ROOF: str = 'unobstructed_slippery_roof'
    OTHER: str = 'other'


class WindDirection(Enum):
    UPWIND: str = 'upwind'
    DOWNWIND: str = 'downwind'
