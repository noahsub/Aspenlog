########################################################################################################################
# safe_data_input.py
# This file contains the input model for the save data endpoint.
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


class SaveDataInput(BaseModel):
    """
    The input model for the save data endpoint
    """

    # The JSON data to save
    json_data: str
    # The id of the save file
    id: Optional[int]
