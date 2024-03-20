########################################################################################################################
# roof_endpoint.py
# This file contains the endpoints used for creating a roof object for a user. It includes the following endpoints:
#   - /roof: POST request to create a roof object for a user
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.roof_manager import process_roof_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_roof
from backend.API.Models.roof_input import RoofInput

########################################################################################################################
# ROUTER
########################################################################################################################

roof_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@roof_router.post("/roof")
def roof_endpoint(roof_input: RoofInput, username: str = Depends(decode_token)):
    """
    Creates a roof object for a user
    :param roof_input: The input data for the roof
    :param username: The username of the user
    :return: A roof object
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the roof data and create a roof object
        roof = process_roof_data(w_roof=roof_input.w_roof, l_roof=roof_input.l_roof, slope=roof_input.slope, uniform_dead_load=roof_input.uniform_dead_load)
        # Store the roof object in the user's memory slot
        set_user_roof(username=username, roof=roof)
        # Return the roof object
        return roof
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
