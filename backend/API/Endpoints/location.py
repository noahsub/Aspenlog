########################################################################################################################
# location.py
# This file contains the endpoints used for setting the location for a user. It includes the following endpoints:
#   - /location: POST request to set the location for a user
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
from backend.API.Managers.location_manager import process_location_data
from backend.API.Managers.user_data_manager import set_user_location, check_user_exists
from backend.API.Models.location_input import LocationInput


########################################################################################################################
# ROUTER
########################################################################################################################

location_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################

@location_router.post("/location")
def location_endpoint(location_input: LocationInput, username: str = Depends(decode_token)):
    """
    Sets the location for a user
    :param location_input: The input data for the location
    :param username: The username of the user
    :return: A location object
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the location data and create a location object
        location = process_location_data(address=location_input.address,
                                         site_designation=location_input.site_designation,
                                         seismic_value=location_input.seismic_value)
        # Store the location object in the user's memory slot
        set_user_location(username=username, location=location)
        # Return the location object
        return location
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
