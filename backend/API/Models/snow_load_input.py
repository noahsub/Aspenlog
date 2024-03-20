########################################################################################################################
# snow_load_input.py
# This file contains the input model for the snow load object.
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


class SnowLoadInput(BaseModel):
    """
    The input model for the snow load object
    """

    # The exposure factor selection
    exposure_factor_selection: str
    # The roof type
    roof_type: str
