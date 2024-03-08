import bpy
import sys
import os

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
from shapes import create_wind_cube
from arrow import create_arrow

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
    except Exception as e:
        print("Failed to decode JSON:", e)
        #with open(json_str, 'r') as file:
            #data = jsonpickle.decode(file)
        #data=json.loads(json_str)
        # REMOVE
        sys.exit(-1)
    rgba_decrement = 1.0/(len(data)-1)
    max_height = 0
    for i in range(len(data)-1):
        height = data[i]['h']
        max_height += height
        r = max(0, 1-(rgba_decrement*i))
        cube = create_wind_cube(height=height, position=i, r=r, g=r)
        
    #add arrow for wind
    create_arrow()

    render_path = "wind_" + str(id) + ".png"

    render.setup_scene(max_height)
    render.render_image(os.path.join(os.path.join(os.path.dirname(module_path), 'output'), render_path))
if __name__ == "__main__":
    main()
