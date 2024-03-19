########################################################################################################################
# user_data_endpoint.py
# This file contains the endpoints used for managing user data. It includes the following endpoints:
#   - /user_data: POST request to get user data
#   - /get_user_profile: POST request to get user profile data
#   - /get_all_user_save_data: POST request to get all user save data
#   - /get_user_save_file: POST request to get a user save file
#   - /set_user_save_data: POST request to set user save data
#   - /set_user_current_save_file: POST request to set the current user save file
#   - /get_user_current_save_file: POST request to get the current user save file
#   - /delete_user_current_save_file: POST request to delete a user save file
#   - /download_user_save_file: POST request to download a user save file
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import io
import json

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_data, get_all_user_save_data, \
    get_user_save_file, set_user_save_data, set_user_current_save_file, get_user_current_save_file, get_user_profile, \
    delete_user_save_file, get_user_save_file_json
from backend.API.Models.save_data_input import SaveDataInput

########################################################################################################################
# ROUTER
########################################################################################################################

user_data_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################

@user_data_router.post("/user_data")
def user_data_endpoint(username: str = Depends(decode_token)):
    """
    Gets user data
    :param username: The username of the user
    :return: The user's data
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Return the user's data
        return get_user_data(username)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_profile")
def get_user_profile_endpoint(username: str = Depends(decode_token)):
    """
    Gets user profile data
    :param username: The username of the user
    :return: The user's profile data
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # A JSON representation of the user's profile data
        return jsonpickle.encode(get_user_profile(username))
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_all_user_save_data")
def get_all_user_save_data_endpoint(username: str = Depends(decode_token)):
    """
    Gets all user save data
    :param username:
    :return:
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Return the user's save data
        return get_all_user_save_data(username)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_save_file")
def get_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    """
    Gets a user save file
    :param id: The id of the save file
    :param username: The username of the user
    :return: The user's save file data
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Return the user's save file data
        return get_user_save_file(username, id)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/set_user_save_data")
def set_user_save_data_endpoint(data: SaveDataInput, username: str = Depends(decode_token)):
    """
    Sets user save data
    :param data: The save data input
    :param username: The username of the user
    :return: The id of the save file
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Set the user's save data
        return set_user_save_data(username, data.json_data, data.id)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/set_user_current_save_file")
def set_user_current_save_file_endpoint(current_save_file: int, username: str = Depends(decode_token)):
    """
    Sets the current user save file
    :param current_save_file: The id of the save file
    :param username: The username of the user
    :return: None
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Set the current user save file
        return set_user_current_save_file(username, current_save_file)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_current_save_file")
def get_user_current_save_file_endpoint(username: str = Depends(decode_token)):
    """
    Gets the current user save file
    :param username: The username of the user
    :return: The id of the current save file
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        return get_user_current_save_file(username)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/delete_user_current_save_file")
def delete_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    """
    Deletes a user save file
    :param id: The id of the save file
    :param username: The username of the user
    :return: None
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        return delete_user_save_file(username, id)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/download_user_save_file")
def download_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    """
    Downloads a user save file
    :param id: The id of the save file
    :param username: The username of the user
    :return: The user's save file data in a JSON file
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Get the user's save file data
        data = get_user_save_file_json(username, id)

        # Create a string of JSON data
        json_str = json.dumps(data)

        # Create an in-memory file
        file_like_object = io.StringIO(json_str)

        # Return a response to download the file
        return StreamingResponse(
            file_like_object,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={username}_{id}_save_file.json"
            },
        )
    # If something goes wrong, raise an error
    except Exception as e:
        return {"error": str(e)}
