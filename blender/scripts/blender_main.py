########################################################################################################################
# blender_main.py
# This file contains the code to create a JSON string to be used in Blender and then runs Blender with created json
# string.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: [https://github.com/alastairsim]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################
import jsonpickle
from blender_object import *
import subprocess
import os

req_file = __file__
req_file = os.path.join(os.path.dirname(req_file), "blender_request.py")


########################################################################################################################
# FUNCTIONS
########################################################################################################################


def create_blender_json(num_zones, heights, loads):
    """
    Create a JSON string to be used in Blender.
    :param num_zones: The number of wind zones.
    :param heights: The heights of the wind zones.
    :param loads: The loads of the wind zones.
    :return: None
    """
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, WindZone(h=heights[i], load=loads[i], position=i).to_dict())

    json_str = jsonpickle.encode(json_str)

    return json_str


########################################################################################################################
# MAIN
########################################################################################################################

json_str = create_blender_json(3, [2, 2, 2], [25, 40, 20])
command = ["blender", "--background", "--python", req_file, "--", "2", json_str]
# print(command)
result = subprocess.run(
    command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
# print(f"ran successfully:", result.stdout.decode())
