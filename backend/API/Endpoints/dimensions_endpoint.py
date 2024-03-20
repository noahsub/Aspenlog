########################################################################################################################
# dimensions_endpoint.py
# This file contains the endpoints used for creating a dimensions object for a user. It includes the following
# endpoints:
#   - /dimensions: POST request to create a dimensions object for a user
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
from backend.API.Managers.dimensions_manager import process_dimension_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_dimensions
from backend.API.Models.dimensions_input import DimensionsInput

########################################################################################################################
# ROUTER
########################################################################################################################

dimensions_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################

@dimensions_router.post("/dimensions")
def dimensions_endpoint(dimensions_input: DimensionsInput, username: str = Depends(decode_token)):
    """
    Creates a dimensions object for a user
    :param dimensions_input: The input data for the dimensions
    :param username: The username of the user
    :return: A dimensions object
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the dimensions data and create a dimensions object
        dimensions = process_dimension_data(width=dimensions_input.width,
                                            height=dimensions_input.height,
                                            eave_height=dimensions_input.eave_height,
                                            ridge_height=dimensions_input.ridge_height)
        # Store the dimensions object in the user's memory slot
        set_user_dimensions(username=username, dimensions=dimensions)
        # Return the dimensions object
        return dimensions
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
