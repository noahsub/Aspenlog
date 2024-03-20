########################################################################################################################
# blender_request.py
# This file contains the code to create a JSON string to be used in Blender and then runs Blender with created json
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: [https://github.com/alastairsim]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import sys
import os

# adding modules to blender path
file = __file__
module_path = os.path.dirname(file)
sys.path.append(module_path)

import subprocess
from concurrent.futures import ThreadPoolExecutor

import json
from blender_object import *
import jsonpickle

########################################################################################################################
# FUNCTIONS
########################################################################################################################


# last argument is JSON string
# json_str = sys.argv[-1]
# id = int(sys.argv[-2])
def create_blender_json(num_zones, heights, loads):
    """
    Create a JSON string to be used in Blender.
    :param num_zones: The number of wind zones.
    :param heights: The heights of the wind zones.
    :param loads: The loads of the wind zones.
    :return: A JSON string to be used in Blender.
    """
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, WindZone(h=heights[i], load=loads[i], position=i).to_dict())

    json_str = jsonpickle.encode(json_str)

    return json_str


# json_str = create_blender_json(3, [2,2,2], [25,40,20])
# id = 3
def run_blender_script(script_path, id, json_str):
    """
    Run a Blender script.
    :param script_path: The path to the Blender script.
    :param id: The id of the Blender script.
    :param json_str: The JSON string to be used in Blender.
    :return: None
    """
    try:
        blender_path = os.environ["BLENDER"]
    except KeyError:
        print("Blender path not found trying default")
        blender_path = "blender"
    args = ["--background", "--python", script_path, "--", str(id), json_str]

    # Combine the Blender path and arguments
    command = [blender_path] + args
    print(command)
    # return(command)
    # Run the command
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"{script_path} ran successfully:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:", e.stderr.decode())


# # Paths to the scripts
# scripts = [os.path.join(module_path, "seismic_cube.py"), os.path.join(module_path, "wind_cube.py")]
# #print(os.path.join(module_path, "seismic_cube.py"))
# #sys.exit(0)
# print("Running:", json_str, "\n", id)
# # Run the scripts in parallel
# with ThreadPoolExecutor(max_workers=2) as executor:
#     results = executor.map(run_blender_script, scripts)
#
#     for result in results:
#         print(result)
