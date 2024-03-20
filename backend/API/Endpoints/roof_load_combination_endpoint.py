########################################################################################################################
# roof_load_combination_endpoint.py
# This file contains the endpoints used for creating a roof load combination object for a user. It includes the
# following endpoints:
#   - /get_roof_load_combinations: POST request to get the roof load combinations for a user
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import json

from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.roof_load_combination_manager import (
    process_roof_load_combination_data,
)
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    get_user_snow_load,
    get_user_building,
)
from backend.API.Models.roof_load_combination_input import RoofLoadCombinationInput

########################################################################################################################
# ROUTER
########################################################################################################################

roof_load_combination_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@roof_load_combination_router.post("/get_roof_load_combinations")
def roof_load_combination_endpoint(
    roof_load_combination_input: RoofLoadCombinationInput,
    username: str = Depends(decode_token),
):
    """
    Gets the roof load combinations for a user
    :param roof_load_combination_input: The input data for the roof load combinations
    :param username: The username of the user
    :return: A JSON object containing the roof load combinations
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # The building object associated with the user
        building = get_user_building(username)
        # Get the snow loads for the user
        snow_load_upwind = get_user_snow_load(username)["upwind"]
        snow_load_downwind = get_user_snow_load(username)["downwind"]
        # Process the roof load combination data and create a roof load combination object
        dataframes = process_roof_load_combination_data(
            building=building,
            snow_load_upwind=snow_load_upwind,
            snow_load_downwind=snow_load_downwind,
            uls_roof_type=roof_load_combination_input.uls_roof_type,
            sls_roof_type=roof_load_combination_input.sls_roof_type,
        )
        # Round the values in the dataframes to 4 decimal places
        upwind_df = dataframes["upwind"].round(4)
        # Get the headers and values for the upwind dataframe
        upwind_headers = [str(x) for x in upwind_df.columns]
        # Find the indices of the companion headers in the upwind dataframe
        upwind_companion_indices = [
            i for i in range(len(upwind_headers)) if "companion" in upwind_headers[i]
        ]
        # Get the values for the upwind dataframe
        upwind_values = [float(x) for x in upwind_df.iloc[0].values]
        # Remove the companion headers and values from the upwind dataframe
        for index in sorted(upwind_companion_indices, reverse=True):
            upwind_headers.pop(index)
            upwind_values.pop(index)
        # Round the values in the dataframes to 4 decimal places
        downwind_df = dataframes["downwind"].round(4)
        # Get the headers and values for the downwind dataframe
        downwind_headers = [str(x) for x in downwind_df.columns]
        # Find the indices of the companion headers in the downwind dataframe
        downwind_companion_indices = [
            i
            for i in range(len(downwind_headers))
            if "companion" in downwind_headers[i]
        ]
        # Get the values for the downwind dataframe
        downwind_values = [float(x) for x in downwind_df.iloc[0].values]
        # Remove the companion headers and values from the downwind dataframe
        for index in sorted(downwind_companion_indices, reverse=True):
            downwind_headers.pop(index)
            downwind_values.pop(index)
        # Return the roof load combinations in a JSON string
        return json.dumps(
            {
                "upwind": [upwind_headers, upwind_values],
                "downwind": [downwind_headers, downwind_values],
            }
        )
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
