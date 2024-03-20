########################################################################################################################
# server_status_endpoint.py
# This file contains the endpoints used for the server status page. It includes the following endpoints:
#   - /server_status: GET request to view the server status page
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from config import get_file_path

########################################################################################################################
# ROUTER
########################################################################################################################

server_status_endpoint = APIRouter()

########################################################################################################################
# ENDPOINTS
########################################################################################################################


@server_status_endpoint.get("/server_status")
def user_data_endpoint():
    """
    Returns the server status page
    :return: The server status page
    """
    try:
        # Get the file path for the server status page
        path = get_file_path('backend/API/Pages/StatusPage/statusPage.html')
        # Return the server status page
        return FileResponse(path)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
