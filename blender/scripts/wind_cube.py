import bpy
import argparse
import sys
sys.path.append('C:\\Users\\Alastair\\Dev\\SEEDA\\blender\\scripts')
sys.path.append('C:\\Users\\Alastair\\Dev\\SEEDA\\blender\\objects')
import render
import os
import jsonpickle
import json
import logging
from blender_object import *
from shapes import create_wind_cube

def create_blender_json(num_zones, heights, loads):
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, HeightZone(h=heights[i], load=loads[i], position=i).to_dict())

    
    json_str = jsonpickle.encode(json_str)
    
    return json_str


def main():
    # Check for args
    if len(sys.argv) < 1:
        print("Usage: blender --background --python blender_request.py -- id '<json_string>'")
        sys.exit(1)
    
    # last argument is JSON string
    json_str = sys.argv[-1]
    id = int(sys.argv[-2])
    #json_str = f'\"{json_str}\"'
    print(json_str)
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
        sys.exit(-1)
    rgba_decrement = 1.0/(len(data)-1)

    for i in range(len(data)-1):
        height = data[i]['h']
        cube = create_wind_cube(height=height, position=i )
        r = max(0, 1-(rgba_decrement*i))

    render_path = "wind_" + str(id) + ".png"

    render.setup_scene()
    render.render_image(os.path.join('C:\\Users\\Alastair\\Dev\\SEEDA\\blender\\output', render_path))
if __name__ == "__main__":
    main()
