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
from shapes import create_wind_cube, set_cube_colour, create_axis, max_height_check
from arrow import create_arrow

def add_load_text(load, location, negative=False, scale=(0.3, 0.3, 0.3), arrow=False):


    font_curve = bpy.data.curves.new(type="FONT", name="numberPlate")
    if negative:
        font_curve.body = str(round(load, 2))
    else:
        try:
            font_curve.body = '+'+str(round(load, 2))
        except:
            font_curve.body = str(load)
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    
    # link to scene collection
    

    # -- Set scale and location
    obj.location = location
    obj.scale = scale
    obj.rotation_euler[0] = math.pi/2
    bpy.context.scene.collection.objects.link(obj)
    #bpy.context.collection.objects.link(obj)
    obj.visible_shadow = False
    if arrow:
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')

        set_cube_colour(obj, (1.0,0.0,1.0,1.0), text=True)
        return 0
    if negative:
        obj.rotation_euler[2] = math.pi/2
        set_cube_colour(obj, (0.0,0.0,1.0,1.0), text=True)
    else:
        set_cube_colour(obj, (1.0,0.0,0.0,1.0), text=True)


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
    heights = max_height_check([i['h'] for i in data[:-1]])

    text_scaling = min(max_hz*0.05, 0.4)
    scale = (text_scaling,)*3
    max_scale_chosen = False
    if scale[0] == 0.4:
        max_scale_chosen = True
    
    for i in range(len(data)-1):
        if i == 0:
            if "Cube" in bpy.data.objects:
                # Deleting Default Cube
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects['Cube'].select_set(True)
                bpy.ops.object.delete()

        height = heights[i]
        position = max_height + height/2
        
        if not max_scale_chosen: 
            text_position_factor = 0.05*height
        else:
            text_position_factor = 0.2
        r = max(0, 1-(rgba_decrement*i))
        cube = create_wind_cube(height=height, position=position, r=r, g=r)
        centre_pos = data[i]['wall_centre_pos']
        centre_neg = data[i]['wall_centre_neg']
        corner_pos = data[i]['wall_corner_pos']
        corner_neg = data[i]['wall_corner_neg']
        add_load_text(centre_pos, (0-text_position_factor, -1.2, position), scale=scale)
        add_load_text(corner_pos, (1-text_position_factor, -1.2, position), scale=scale)
        add_load_text(corner_pos, (-1-text_position_factor, -1.2, position), scale=scale)

        add_load_text(centre_neg, (1.15, 0-text_position_factor, position-0.5), negative=True, scale=scale)
        add_load_text(corner_neg, (1.15, -1-text_position_factor, position-0.5), negative=True, scale=scale)
        add_load_text(corner_neg, (1.15, 0.9-text_position_factor, position-0.5), negative=True, scale=scale)
        max_height += height
    #add arrow for wind
    if len(data) == 1: 
        max_height = max_height*4
    create_arrow(loc_x=0, loc_y=-3)
    add_load_text("Wind Direction", (0, -3.5, 0.5), scale=scale, arrow=True)
    create_axis(location=(-3, -max_height/2, max_height/2))
    render_path = "wind_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path('backend/output')
    render.render_image(os.path.join(output_path, render_path))
if __name__ == "__main__":
    main()
