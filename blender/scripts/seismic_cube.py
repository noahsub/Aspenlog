import bpy
import sys
import math
import os



# adding modules to blender path
file = __file__
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
module_path = os.path.dirname(file)
#print(PROJECT_DIR)
sys.path.append(module_path)
sys.path.append(PROJECT_DIR)
from config import get_file_path
import render
import os
import jsonpickle
from shapes import create_seismic_cube, set_cube_colour, create_axis


def color_based_on_load(load_value, max_load):
    # Ensure the load value is clamped between 0 and 100
    load_value = max(0, min(max_load, load_value))
    
    # Normalize the load value to a range between 0 and 1
    normalized_load = load_value / max_load
    
    # Interpolate between green and red based on the load value
    # Green to Red transition: (0, 1, 0) to (1, 0, 0)
    r = normalized_load
    g = 1 - normalized_load
    b = 0 # - normalized_load
    a=1.0
    return (r, g, b, a)

def add_load_text(load, z, scale):


    font_curve = bpy.data.curves.new(type="FONT", name="numberPlate")
    font_curve.body = str(round(load, 2))
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)

    # -- Set scale and location
    obj.location = (1, -1.1 , z)
    obj.scale = (scale,scale,scale)
    obj.rotation_euler[0] = math.pi/2
    bpy.context.scene.collection.objects.link(obj)
    set_cube_colour(obj, (1.0,0.0,1.0,1.0))
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
    max_hz = max([i['h'] for i in data[:-1]])
    max_load = max([i['load'] for i in data[:-1]])

    # text scaling
    scale = max_hz*0.1
    for i in range(len(data)-1):
        if i == 0:
            
            if "Cube" in bpy.data.objects:
                # Deleting Default Cube
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects['Cube'].select_set(True)
                bpy.ops.object.delete()
        height = data[i]['h']
        position = max_height + height/2
        cube = create_seismic_cube(height=height, position=position )
        load_value = data[i]['load']
        set_cube_colour(cube, color_based_on_load(load_value, max_load))
        add_load_text(load_value, max_height, scale)
        max_height += height
    create_axis(location=(-3, -max_height/2, max_height/2))
    render_path = "seismic_" + str(id) + ".png"

    render.setup_scene(max_height)
    output_path = get_file_path('backend/output')
    render.render_image(os.path.join(output_path, render_path))

if __name__ == "__main__":
    main()