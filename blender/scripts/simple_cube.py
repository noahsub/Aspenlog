########################################################################################################################
# simple_cube.py
# This file contains the code to create a simple cube in Blender.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: [https://github.com/alastairsim]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import bpy
import sys
import os

# adding modules to blender path
file = __file__
PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
module_path = os.path.dirname(file)
sys.path.append(module_path)
sys.path.append(PROJECT_DIR)
from config import get_file_path


import render
import os
import jsonpickle
import json
import logging
from blender_object import *
from shapes import create_simple_cube

########################################################################################################################
# MAIN
########################################################################################################################


def main():

    # last argument is JSON string
    json_str = sys.argv[-1]
    id = str(sys.argv[-2])
    try:
        # Parse the JSON string
        data = jsonpickle.decode(json_str)
        # Now you can use the data object as needed, for example:
        print("Data received:", data)
    except Exception as e:
        print("Failed to decode JSON:", e)

    max_possible_height = 30  # 58.29
    max_height = min(data["total_elevation"], max_possible_height)
    angle = data["roof_angle"]
    print("Creating Simple Cube")
    create_simple_cube(angle_degrees=angle, total_height=max_height)

    render_path = "simple_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path("backend/output")
    render.render_image(os.path.join(output_path, render_path))


if __name__ == "__main__":
    main()
