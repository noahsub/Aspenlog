########################################################################################################################
# wind_load_endpoint.py
# This file contains the endpoints used for creating a wind load object for a user. It includes the following endpoints:
#   - /set_wind_load: POST request to create a wind load object for a user
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
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    get_user_building,
    get_user_importance_category,
    get_user_location,
)
from backend.API.Managers.wind_load_manager import process_wind_load_data
from backend.API.Models.wind_load_input import WindLoadInput

########################################################################################################################
# ROUTER
########################################################################################################################

wind_load_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@wind_load_router.post("/set_wind_load")
def set_wind_load_endpoint(
    wind_load_input: WindLoadInput, username: str = Depends(decode_token)
):
    """
    Creates a wind load object for a user
    :param wind_load_input: The input data for the wind load
    :param username: The username of the user
    :return: None
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # The user's building data
        building = get_user_building(username=username)
        # The user's importance factor
        importance_factor = get_user_importance_category(username=username)
        # The user's location
        location = get_user_location(username=username)
        # Process the wind load data and create wind load objects
        for height_zone in building.height_zones:
            i = height_zone.zone_num - 1
            process_wind_load_data(
                building=building,
                height_zone=height_zone,
                importance_category=importance_factor,
                location=location,
                ct=wind_load_input.ct[i],
                exposure_factor=wind_load_input.exposure_factor[i],
                internal_pressure_category=wind_load_input.internal_pressure_category[
                    i
                ],
                manual_ce_cei=wind_load_input.manual_ce_cei[i],
            )
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
