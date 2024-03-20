########################################################################################################################
# roof_input.py
# This file contains the input model for the roof object.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from pydantic import BaseModel


########################################################################################################################
# MODEL
########################################################################################################################

class RoofInput(BaseModel):
    """
    The input model for the roof object
    """
    # The width of the roof
    w_roof: float
    # The length of the roof
    l_roof: float
    # The slope of the roof
    slope: float
    # The dead load of the roof
    uniform_dead_load: float
