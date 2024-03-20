########################################################################################################################
# wind_load_input.py
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

from typing import Optional, List

from pydantic import BaseModel

########################################################################################################################
# MODEL
########################################################################################################################

class WindLoadInput(BaseModel):
    """
    The input model for the wind load object
    """
    # The topographic factor
    ct: List[float]
    # The exposure factor
    exposure_factor: List[str]
    # The manual exposure factor for intermediate exposure
    manual_ce_cei: List[Optional[float]]
    # The internal pressure category
    internal_pressure_category: List[str]
