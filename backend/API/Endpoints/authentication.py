########################################################################################################################
# authentication.py
# This file contains the endpoints for the authentication API. It includes the following endpoints:
#   - /register: POST request to register a new user
#   - /login: POST request to login an existing user
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from fastapi import APIRouter, HTTPException, status

from backend.API.Managers.authentication_manager import signup, login
from backend.API.Models.login_input import LoginInput
from backend.API.Models.register_input import RegisterInput

########################################################################################################################
# ROUTER
########################################################################################################################

authentication_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################

@authentication_router.post("/register")
def register_endpoint(register_input: RegisterInput):
    """
    Registers a new user
    :param register_input: The input data for the new user
    :return: A message indicating whether the user was registered successfully
    """
    # Check if the user was registered successfully
    if signup(register_input.username, register_input.first_name, register_input.last_name, register_input.password,
              register_input.email):
        return f"user '{register_input.username}' has been registered successfully"
    # If the user was not registered successfully, raise an error
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


@authentication_router.post("/login")
def register_endpoint(login_input: LoginInput):
    """
    Logs in an existing user
    :param login_input: The input data for the user
    :return: An API key if the user was logged in successfully
    """
    # The API key retrieved from the login function
    api_key = login(login_input.username, login_input.password)
    # If no API key was retrieved, raise an error
    if api_key is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # If an API key was retrieved, return the API key
    else:
        return api_key
