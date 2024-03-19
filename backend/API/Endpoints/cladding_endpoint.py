########################################################################################################################
# cladding_endpoint.py
# This file contains the endpoints used for creating a cladding object for a user. It includes the following endpoints:
#   - /cladding: POST request to create a cladding object for a user
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
from backend.API.Managers.cladding_manager import process_cladding_data
from backend.API.Managers.user_data_manager import set_user_cladding, check_user_exists
from backend.API.Models.cladding_input import CladdingInput

########################################################################################################################
# ROUTER
########################################################################################################################

cladding_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@cladding_router.post("/cladding")
def cladding_endpoint(cladding_input: CladdingInput, username: str = Depends(decode_token)):
    """
    Creates a cladding object for a user
    :param cladding_input: The input data for the cladding
    :param username: The username of the user
    :return: A cladding object
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the cladding data and create a cladding object
        cladding = process_cladding_data(c_top=cladding_input.c_top, c_bot=cladding_input.c_bot)
        # Store the cladding object in the user's memory slot
        set_user_cladding(username=username, cladding=cladding)
        # Return the cladding object
        return cladding
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
