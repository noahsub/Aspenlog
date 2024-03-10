import bpy
import sys
import os

from config import get_file_path

# adding modules to blender path
file = __file__
module_path = os.path.dirname(file)
sys.path.append(module_path)


import render
import os
import jsonpickle
import json
import logging
from blender_object import *
from shapes import create_simple_cube

def main():
    
    # last argument is JSON string
    json_str = sys.argv[-1]
    id = int(sys.argv[-2])
    try:
        # Parse the JSON string
        data = jsonpickle.decode(json_str)
        # Now you can use the data object as needed, for example:
        print("Data received:", data)
    except Exception as e:
        print("Failed to decode JSON:", e)
        

    max_height = data['total_elevation']
    angle = data['roof_angle']
    create_simple_cube(angle_degrees=angle, total_height=max_height)

    render_path = "simple_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path('backend/output')
    render.render_image(os.path.join(output_path, render_path))

if __name__ == "__main__":
    main()

