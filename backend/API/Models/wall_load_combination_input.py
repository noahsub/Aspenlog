########################################################################################################################
# walls_load_combination_input.py
# This file contains the input model for the wall load combination object.
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


class WallLoadCombinationInput(BaseModel):
    """
    The input model for the wall load combination object
    """

    # The uls wall type
    uls_wall_type: str
    # The sls wall type
    sls_wall_type: str
