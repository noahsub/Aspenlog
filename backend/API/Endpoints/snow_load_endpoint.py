########################################################################################################################
# snow_load_endpoint.py
# This file contains the endpoints used for creating a snow load object for a user. It includes the following endpoints:
#   - /set_snow_load: POST request to create a snow load object for a user
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.snow_load_manager import process_snow_load_data
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_importance_category, \
    get_user_location, set_user_snow_load
from backend.API.Models.snow_load_input import SnowLoadInput

########################################################################################################################
# ROUTER
########################################################################################################################

snow_load_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@snow_load_router.post("/set_snow_load")
def set_snow_load_endpoint(snow_load_input: SnowLoadInput, username: str = Depends(decode_token)):
    """
    Creates a snow load object for a user
    :param snow_load_input: The input data for the snow load
    :param username: The username of the user
    :return: A JSON representation of the snow load object
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # The building associated with the user
        building = get_user_building(username=username)
        # The importance factor for the user
        importance_factor = get_user_importance_category(username=username)
        # The location of the user
        location = get_user_location(username=username)
        # Process the snow load data and create a snow load object
        snow_load = process_snow_load_data(building=building, location=location, importance_category=importance_factor, exposure_factor_selection=snow_load_input.exposure_factor_selection, roof_type=snow_load_input.roof_type)
        # Store the snow load object in the user's memory slot
        set_user_snow_load(username=username, snow_load=snow_load)
        # Return the snow load object as a JSON string
        return jsonpickle.encode(snow_load)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
