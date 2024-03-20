########################################################################################################################
# roofs_load_combination_input.py
# This file contains the input model for the roof load combination object.
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

class RoofLoadCombinationInput(BaseModel):
    """
    The input model for the roof load combination object
    """
    # The ULS and SLS roof types
    uls_roof_type: str
    sls_roof_type: str
