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
from shapes import create_seismic_cube, set_cube_colour

def color_based_on_load(load_value, max_load):
    # Ensure the load value is clamped between 0 and 100
    load_value = max(0, min(max_load, load_value))
    
    # Normalize the load value to a range between 0 and 1
    normalized_load = load_value / max_load
    
    # Interpolate between green and red based on the load value
    # Green to Red transition: (0, 1, 0) to (1, 0, 0)
    r = normalized_load
    g = 1 - normalized_load
    b = 0
    a=1.0
    return (r, g, b, a)

def main():
    # Check for args
    if len(sys.argv) < 1:
        print("Usage: blender --background --python blender_request.py -- id '<json_string>'")
        sys.exit(1)

    # last argument is JSON string
    json_str = sys.argv[-1]
    id = int(sys.argv[-2])

    try:
        # Parse the JSON string
        data = jsonpickle.decode(json_str)
        
        # Now you can use the data object as needed, for example:
        print("Data received:", data)
    except jsonpickle.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        sys.exit(1)
    max_height = 0
    max_load = max([i['load'] for i in data[:-1]])
    for i in range(len(data)-1):
        height = data[i]['h']
        max_height += height
        cube = create_seismic_cube(height=height, position=i )
        load_value = data[i]['load']
        set_cube_colour(cube, color_based_on_load(load_value, max_load))

    render_path = "seismic_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path('backend/output')
    render.render_image(os.path.join(output_path, render_path))

if __name__ == "__main__":
    main()