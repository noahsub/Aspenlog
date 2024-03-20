########################################################################################################################
# location_input.py
# This file contains the input model for the location object.
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


class LocationInput(BaseModel):
    """
    The input model for the location object
    """

    # The address of the building
    address: str
    # The site designation type (xv, or xs)
    site_designation: str
    # The seismic value of the site (int for xv, str for xs)
    seismic_value: int | str
