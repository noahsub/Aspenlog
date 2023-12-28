########################################################################################################################
# wind_constants.py
# This file contains the constants and enums pertaining to wind
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

# The wind gust factor
GUST_FACTOR = 2.5

########################################################################################################################
# ENUMS
########################################################################################################################


class WindExposureFactorSelections(Enum):
    """
    Enum for the wind exposure factor selections
    """
    OPEN: str = 'open'
    ROUGH: str = 'rough'
    INTERMEDIATE: str = 'intermediate'


class InternalPressureSelections(Enum):
    """
    Enum for the internal pressure selections
    """
    ENCLOSED: str = 'enclosed'
    PARTIALLY_ENCLOSED: str = 'partially_enclosed'
    LARGE_OPENINGS: str = 'large_openings'
