########################################################################################################################
# snow_constants.py
# This file contains the constants and enums pertaining to snow
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
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
