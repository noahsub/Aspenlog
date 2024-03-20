########################################################################################################################
# dimensions_input.py
# This file contains the input model for the dimensions object.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from typing import Optional
from pydantic import BaseModel


########################################################################################################################
# MODEL
########################################################################################################################


class DimensionsInput(BaseModel):
    """
    The input model for the dimensions object
    """

    # The width of the building
    width: float
    # The height of the building
    height: Optional[float]
    # The eave height of the building
    eave_height: Optional[float]
    # The ridge height of the building
    ridge_height: Optional[float]
