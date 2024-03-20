########################################################################################################################
# building_endpoint.py
# This file contains the endpoints used for creating a building object for a user. It includes the following endpoints:
#   - /building: POST request to create a building object for a user
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
from backend.API.Managers.building_manager import process_building_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_building
from backend.API.Models.building_input import BuildingInput

########################################################################################################################
# ROUTER
########################################################################################################################

building_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@building_router.post("/building")
def building_endpoint(
    building_input: BuildingInput, username: str = Depends(decode_token)
):
    """
    Creates a building object for a user
    :param building_input: The input data for the building
    :param username: The username of the user
    :return: A JSON string of the building object
    """
    # Check if the user exists
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the building data and create a building object
        building = process_building_data(
            num_floor=building_input.num_floor,
            h_opening=building_input.h_opening,
            zones=building_input.zones,
            materials=building_input.materials,
            username=username,
        )
        # Store the building object in the user's memory slot
        set_user_building(username=username, building=building)
        # Return the building object as a JSON string
        return jsonpickle.encode(building)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
