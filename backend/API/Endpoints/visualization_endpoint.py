########################################################################################################################
# visualization_endpoint.py
# This file contains the endpoints used for generating visualizations. It includes the following endpoints:
#   - /bar_chart: POST request to generate a bar chart
#   - /load_model: POST request to generate a load model
#   - /simple_model: POST request to generate a simple model
#   - /get_bar_chart: GET request to get a bar chart
#   - /get_wind_load_model: GET request to get a wind load model
#   - /get_seismic_load_model: GET request to get a seismic load model
#   - /get_simple_model: GET request to get a simple model
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import uuid

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    get_user_building,
    get_user_snow_load,
)
from backend.API.Models.simple_model_input import SimpleModelInput
from backend.visualizations.load_combination_bar_chart import generate_bar_chart
from blender.scripts.blender_object import WindZone, SeismicZone
from blender.scripts.blender_request import run_blender_script
from config import get_file_path

########################################################################################################################
# ROUTER
########################################################################################################################

visualization_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@visualization_router.post("/bar_chart")
def generate_bar_chart_endpoint(username: str = Depends(decode_token)):
    """
    Generates a 3D bar chart for the load combinations for a height zone
    :param username: The username of the user
    :return: A JSON object containing the id of the bar chart and the number of bar charts generated
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Generate a unique id for the bar chart
        id = str(uuid.uuid4())
        # Get the user's building and snow load
        building = get_user_building(username)
        snow_load = get_user_snow_load(username)["upwind"]
        # Generate the bar chart
        num_generated = generate_bar_chart(
            id=id, building=building, snow_load=snow_load
        )
        # Return the id and the number of bar charts generated
        return jsonpickle.encode({"id": id, "num_bar_charts": num_generated})
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.post("/load_model")
def generate_load_model_endpoint(username: str = Depends(decode_token)):
    """
    Generates a load model for a user's building
    :param username: The username of the user
    :return: The id of the load model
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Generate a unique id for the load model
        id = str(uuid.uuid4())
        # Get the user's building
        building = get_user_building(username=username)
        # Get the height zones of the building
        height_zones = building.height_zones
        # Create a list of wind and seismic cubes for the building
        wind_cubes = []
        seismic_cubes = []
        # Initialize the previous elevation
        prev_elevation = 0
        # For each height zone, create a wind and seismic cube
        for height_zone in sorted(height_zones, key=lambda x: x.zone_num):
            wind_cubes.append(
                WindZone(
                    h=height_zone.elevation - prev_elevation,
                    wall_centre_pos=height_zone.wind_load.get_zone(4).pressure.pos_uls,
                    wall_centre_neg=height_zone.wind_load.get_zone(4).pressure.neg_uls,
                    wall_corner_pos=height_zone.wind_load.get_zone(5).pressure.pos_uls,
                    wall_corner_neg=height_zone.wind_load.get_zone(5).pressure.neg_uls,
                ).to_dict()
            )
            seismic_cubes.append(
                SeismicZone(
                    h=height_zone.elevation - prev_elevation,
                    load=height_zone.seismic_load.vp,
                ).to_dict()
            )
            # Update the previous elevation
            prev_elevation = height_zone.elevation

        # Convert the wind and seismic cubes to JSON
        json_wind = jsonpickle.encode(wind_cubes)
        path_wind = get_file_path("blender/scripts/wind_cube.py")
        run_blender_script(script_path=path_wind, id=id, json_str=json_wind)

        json_seismic = jsonpickle.encode(seismic_cubes)
        path_seismic = get_file_path("blender/scripts/seismic_cube.py")
        run_blender_script(script_path=path_seismic, id=id, json_str=json_seismic)
        # Return the id of the load models
        return jsonpickle.encode(id)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.post("/simple_model")
def generate_simple_model_endpoint(
    simple_model_input: SimpleModelInput, username: str = Depends(decode_token)
):
    """
    Generates a simple model for a user's building
    :param simple_model_input: The input data for the simple model
    :param username: The username of the user
    :return: The id of the simple model
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Generate a unique id for the simple model
        id = str(uuid.uuid4())
        # Get the total elevation and roof angle
        total_elevation = simple_model_input.total_elevation
        roof_angle = simple_model_input.roof_angle
        # Convert the total elevation and roof angle to JSON
        json_simple = jsonpickle.encode(
            {"total_elevation": total_elevation, "roof_angle": roof_angle}
        )
        # Generate the simple model
        path_simple = get_file_path("blender/scripts/simple_cube.py")
        run_blender_script(script_path=path_simple, id=id, json_str=json_simple)
        # Return the id of the simple model
        return jsonpickle.encode(id)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_bar_chart")
def get_bar_chart_endpoint(id: str, zone_num: int):
    """
    Gets a bar chart
    :param id: The id of the bar chart
    :param zone_num: The numerical identifier of the height zone
    :return: The bar chart as a png file
    """
    try:
        # Get the path of the bar chart
        output_path = get_file_path(f"backend/output/bar_chart_hz_{zone_num}_{id}.png")
        # Return the bar chart as a png file
        return FileResponse(output_path)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_wind_load_model")
def get_wind_load_model_endpoint(id: str):
    """
    Gets a wind load model
    :param id: The id of the wind load model
    :return: The wind load model as a png file
    """
    try:
        # Get the path of the wind load model
        output_path = get_file_path(f"backend/output/wind_{id}.png")
        # Return the wind load model as a png file
        return FileResponse(output_path)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_seismic_load_model")
def get_seismic_load_model_endpoint(id: str):
    """
    Gets a seismic load model
    :param id: The id of the seismic load model
    :return: The seismic load model as a png file
    """
    try:
        # Get the path of the seismic load model
        output_path = get_file_path(f"backend/output/seismic_{id}.png")
        # Return the seismic load model as a png file
        return FileResponse(output_path)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_simple_model")
def get_simple_model_endpoint(id: str):
    """
    Gets a simple model
    :param id: The id of the simple model
    :return: The simple model as a png file
    """
    try:
        # Get the path of the simple model
        output_path = get_file_path(f"backend/output/simple_{id}.png")
        # Return the simple model as a png file
        return FileResponse(output_path)
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
