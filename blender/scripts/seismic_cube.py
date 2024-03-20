########################################################################################################################
# render.py
# This file contains the code to set up the scene and render the image in Blender.
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
import math
import os


# adding modules to blender path
file = __file__
PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
module_path = os.path.dirname(file)
# print(PROJECT_DIR)
sys.path.append(module_path)
sys.path.append(PROJECT_DIR)
from config import get_file_path
import render
import os
import jsonpickle
from shapes import create_seismic_cube, set_cube_colour, create_axis, max_height_check


########################################################################################################################
# FUNCTIONS
########################################################################################################################


def color_even_odd(index):
    """
    switches opacity for even and odd index
    :param index: index of the cube
    :return: rgba tuple
    """
    if index % 2 == 0:
        return (0.0, 0.2, 0.0, 0.5)
    else:
        return (0.0, 0.4, 0.0, 0.3)


def color_based_on_load(load_value, max_load):
    """
    Interpolates between green and red based on the load value.
    :param load_value: The load value.
    :param max_load: The maximum load value.
    :return: An RGBA tuple.
    """
    # Ensure the load value is clamped between 0 and 100
    load_value = max(0, min(max_load, load_value))

    # Normalize the load value to a range between 0 and 1
    normalized_load = load_value / max_load

    # Interpolate between green and red based on the load value
    # Green to Red transition: (0, 1, 0) to (1, 0, 0)
    r = normalized_load
    g = 1  # - normalized_load
    b = 0  # - normalized_load
    a = 1.0
    return (r, g, b, a)


def add_load_text(load, z, scale, location=(-0.5, -1.1), rotation=(math.pi / 2, 0, 0)):
    """
    Add a text object to the scene.
    :param load: The load value.
    :param z: The z location of the text object.
    :param scale: The scale of the text object.
    :param location: The location of the text object.
    :param rotation: The rotation of the text object.
    :return: None
    """
    font_curve = bpy.data.curves.new(type="FONT", name="numberPlate")
    try:
        font_curve.body = str(round(load, 2))
    except TypeError:
        font_curve.body = str(load)

    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)

    # -- Set scale and location
    obj.location = (location[0], location[1], z)
    obj.scale = (scale, scale, scale)
    obj.rotation_euler = rotation
    bpy.context.scene.collection.objects.link(obj)
    obj.visible_shadow = False
    set_cube_colour(obj, (1.0, 0.0, 1.0, 1.0), text=True)


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
    except jsonpickle.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    max_height = 0
    max_hz = max([i["h"] for i in data])
    max_load = max([i["load"] for i in data])
    heights = max_height_check([i["h"] for i in data])

    # text scaling
    scale = max_hz * 0.05
    for i in range(len(data)):
        if i == 0:

            if "Cube" in bpy.data.objects:
                # Deleting Default Cube
                bpy.ops.object.select_all(action="DESELECT")
                bpy.data.objects["Cube"].select_set(True)
                bpy.ops.object.delete()
        height = heights[i]
        position = max_height + height / 2
        cube = create_seismic_cube(height=height, position=position)
        load_value = data[i]["load"]
        set_cube_colour(cube, color_even_odd(i), emit=True)

        cube.visible_shadow = False
        add_load_text(load_value, position, scale)
        max_height += height

    add_load_text(
        load="Seismic Load (kPa) \n *Wall Colour is to Distinguish Zones ",
        z=1,
        location=(0.8, -3),
        scale=0.5,
        rotation=(math.pi / 2, 0, math.pi / 4),
    )
    create_axis(location=(-3, -max_height / 2, max_height / 2))
    render_path = "seismic_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path("backend/output")
    render.render_image(os.path.join(output_path, render_path))


if __name__ == "__main__":
    main()
