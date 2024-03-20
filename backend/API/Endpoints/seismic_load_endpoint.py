########################################################################################################################
# set_seismic_load_endpoint.py
# This file contains the endpoints used for creating a seismic load object for a user. It includes the following
# endpoints:
#   - /set_seismic_load: POST request to create a seismic load object for a user
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
from backend.API.Managers.seismic_load_manager import process_seismic_load_data
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    get_user_building,
    get_user_importance_category,
    get_user_location,
)
from backend.API.Models.seismic_load_input import SeismicLoadInput

########################################################################################################################
# ROUTER
########################################################################################################################

seismic_load_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@seismic_load_router.post("/set_seismic_load")
def set_seismic_load_endpoint(
    seismic_load_input: SeismicLoadInput, username: str = Depends(decode_token)
):
    """
    Creates a seismic load object for a user
    :param seismic_load_input: The input data for the seismic load
    :param username: The username of the user
    :return: None
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the seismic load data and create a seismic load object
        building = get_user_building(username=username)
        # Get the user's importance factor
        importance_factor = get_user_importance_category(username=username)
        # Get the user's building location
        location = get_user_location(username=username)
        # Process the seismic load data
        process_seismic_load_data(
            building=building,
            location=location,
            importance_category=importance_factor,
            ar=seismic_load_input.ar,
            rp=seismic_load_input.rp,
            cp=seismic_load_input.cp,
        )
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
