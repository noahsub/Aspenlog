########################################################################################################################
# load_constants.py
# This file contains the constants and enums pertaining to the load types.
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
# ENUMS
########################################################################################################################


class LoadTypes(Enum):
    """
    Enum for the load types
    """

    WIND: str = "WIND"
    SNOW: str = "SNOW"
    SEISMIC: str = "SEISMIC"
