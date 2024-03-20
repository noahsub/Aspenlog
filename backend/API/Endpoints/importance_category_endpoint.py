########################################################################################################################
# importance_category_endpoint.py
# This file contains the endpoints used for setting the importance category for a user. It includes the following
# endpoints:
#   - /importance_category: POST request to set the importance category for a user
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
from backend.API.Managers.importance_category_manager import (
    process_importance_category_data,
)
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    set_user_importance_category,
)
from backend.API.Models.importance_category_input import ImportanceCategoryInput

########################################################################################################################
# ROUTER
########################################################################################################################

importance_category_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@importance_category_router.post("/importance_category")
def importance_category_endpoint(
    importance_category_input: ImportanceCategoryInput,
    username: str = Depends(decode_token),
):
    """
    Sets the importance category for a user
    :param importance_category_input: The input data for the importance category
    :param username: The username of the user
    :return: The importance category
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Process the importance category data and create an importance category object
        importance_category = process_importance_category_data(
            importance_category_input.importance_category
        )
        # Store the importance category object in the user's memory slot
        set_user_importance_category(
            username=username, importance_category=importance_category
        )
        # Return the importance category object
        return importance_category
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
