import bpy
import sys
import os
import math

# adding modules to blender path
file = __file__
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
from shapes import create_wind_cube, set_cube_colour
from arrow import create_arrow

def add_load_text(load, location, negative=False, scale=(0.3, 0.3, 0.3)):


    font_curve = bpy.data.curves.new(type="FONT", name="numberPlate")
    if negative:
        font_curve.body = str(round(load, 2))
    else:
        font_curve.body = '+'+str(round(load, 2))
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)

    # -- Set scale and location
    obj.location = location
    obj.scale = scale
    obj.rotation_euler[0] = math.pi/2
    bpy.context.scene.collection.objects.link(obj)
    if negative:
        obj.rotation_euler[2] = math.pi/2
        set_cube_colour(obj, (0.0,0.0,1.0,1.0), text=True)
    else:
        set_cube_colour(obj, (0.0,1.0,0.0,1.0), text=True)


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
        
    rgba_decrement = 1.0/(len(data)-1)
    max_height = 0
    max_hz = max([i['h'] for i in data[:-1]])
    scale = (max_hz*0.1,)*3
    for i in range(len(data)-1):
        if i == 0:
            if "Cube" in bpy.data.objects:
                # Deleting Default Cube
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects['Cube'].select_set(True)
                bpy.ops.object.delete()

        height = data[i]['h']
        position = max_height + height/2
        r = max(0, 1-(rgba_decrement*i))
        cube = create_wind_cube(height=height, position=position, r=r, g=r)
        centre_pos = data[i]['wall_centre_pos']
        centre_neg = data[i]['wall_centre_neg']
        corner_pos = data[i]['wall_corner_pos']
        corner_neg = data[i]['wall_corner_neg']
        add_load_text(centre_pos, (-0.3, -1.2, position), scale=scale)
        add_load_text(corner_pos, (0.7, -1.2, position), scale=scale)
        add_load_text(corner_pos, (-1.3, -1.2, position), scale=scale)

        add_load_text(centre_neg, (1.15, 0, position-0.5), negative=True, scale=scale)
        add_load_text(corner_neg, (1.15, -1.2, position-0.5), negative=True, scale=scale)
        add_load_text(corner_neg, (1.15, 0.8, position-0.5), negative=True, scale=scale)
        max_height += height
    #add arrow for wind
    if len(data) == 1: 
        max_height = max_height*4
    create_arrow(loc_x=0, loc_y=-3)

    render_path = "wind_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path('backend/output')
    render.render_image(os.path.join(output_path, render_path))
if __name__ == "__main__":
    main()
