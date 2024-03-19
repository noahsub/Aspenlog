########################################################################################################################
# walls_load_combination_endpoint.py
# This file contains the endpoints used for creating a wall load combination object for a user. It includes the
# following endpoints:
#   - /get_wall_load_combinations: POST request to create a wall load combination object for a user
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
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_snow_load
from backend.API.Managers.wall_load_combination_manager import process_wall_load_combination_data
from backend.API.Models.wall_load_combination_input import WallLoadCombinationInput

########################################################################################################################
# ROUTER
########################################################################################################################

wall_load_combination_router = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@wall_load_combination_router.post("/get_wall_load_combinations")
def wall_load_combination_endpoint(wall_load_combination_input: WallLoadCombinationInput,
                                   username: str = Depends(decode_token)):
    """
    Creates a wall load combination dataframe based on the user's data
    :param wall_load_combination_input: The input data for the wall load combination
    :param username: The username of the user
    :return: A JSON object containing the wall load combination dataframe
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # The user's building data
        building = get_user_building(username)
        # The user's snow load data
        snow_load = get_user_snow_load(username)['upwind']
        # Process the wall load combination data and create a wall load combination dataframe
        df = process_wall_load_combination_data(building=building, snow_load=snow_load,
                                                uls_wall_type=wall_load_combination_input.uls_wall_type,
                                                sls_wall_type=wall_load_combination_input.sls_wall_type).round(4)
        # Check if the 'companion' column exists and drop it
        if 'companion' in df.columns:
            df = df.drop(columns=['companion'])
        # Convert the dataframe to a JSON object
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        # Return the JSON object
        return parsed
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
