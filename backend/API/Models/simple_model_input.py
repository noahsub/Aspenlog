########################################################################################################################
# simple_model_input.py
# This file contains the input model for the simple model object.
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


class SimpleModelInput(BaseModel):
    """
    The input model for the simple model object
    """

    # The total elevation of the building
    total_elevation: float
    # The roof angle of the building
    roof_angle: float
