########################################################################################################################
# height_zones_endpoint.py
# This file contains the endpoints used for getting the height zones for a user's building. It includes the following
# endpoints:
#   - /get_height_zones: POST request to get the height zones for a user's building
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
from fastapi import HTTPException, Depends, APIRouter

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import get_user_building, check_user_exists

########################################################################################################################
# ROUTER
########################################################################################################################

height_zone_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@height_zone_router.post("/get_height_zones")
def get_height_zones_endpoint(username: str = Depends(decode_token)):
    """
    Gets the height zones for a user's building
    :param username: The username of the user
    :return: A JSON string representation of the height zones
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Get the user's building
        building = get_user_building(username=username)
        # Create a dictionary of the height zones
        height_zones = {}
        for zone in building.height_zones:
            height_zones[zone.zone_num] = zone
        # Return the height zones as a JSON string
        return jsonpickle.encode(height_zones)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
