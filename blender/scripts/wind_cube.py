import bpy
import argparse
import sys
import render
import os

import logging

# Configure logging
log_file_path = os.path.join('./logs', 'blender_script.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def create_cube(length=2.0, width=2.0, height=2.0, position=0):
   

    cube_x = length * 0.9
    cube_y = width * 0.9
    cube_z = height * 0.9
    
    block_z = position*cube_z
    # Add a cube
    bpy.ops.mesh.primitive_cube_add(scale=(cube_x, cube_y, cube_z), size=1, enter_editmode=False, location=(0, 0, block_z))

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    # Apply the scaling transformation
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Enter edit mode to modify the cube
    bpy.ops.object.editmode_toggle()

    # positive x
    bpy.ops.mesh.primitive_cube_add(scale=(length*0.1/2, cube_y/2, cube_z/2), enter_editmode=True, location=(cube_x/2+length*0.05, 0, block_z))

    bpy.ops.mesh.primitive_cube_add(scale=(length*0.1/2, cube_y/2, cube_z/2), enter_editmode=True, location=(-cube_x/2-length*0.05, 0, block_z))

    bpy.ops.mesh.primitive_cube_add(scale=(cube_x/2, width*0.1/2, cube_z/2), enter_editmode=True, location=(0, cube_y/2+width*0.05, block_z))
    bpy.ops.mesh.primitive_cube_add(scale=(cube_x/2,width*0.1/2, cube_z/2), enter_editmode=True, location=(0,-cube_y/2-width*0.05, block_z))
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False,  location=(cube_x/2+length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False,  location=(-cube_x/2-length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False,  location=(cube_x/2+length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False,  location=(-cube_x/2-length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))

def set_cube_colour():
    # Select the object by name, the default cube
    cube = bpy.data.objects['Cube']

    # Create a new material
    mat = bpy.data.materials.new(name="CustomMaterial")

    # Enable 'Use nodes':
    mat.use_nodes = True

    # Access the principled BSDF, the default shader for new materials
    principled_bsdf = mat.node_tree.nodes.get('Principled BSDF')

    # Set the color - in RGBA format, from 0.0 to 1.0
    # red
    principled_bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Red

    # Assign the material to the object
    if cube.data.materials:
        # If the object already has material slots
        cube.data.materials[0] = mat
    else:
        # If the object has no material slots
        cube.data.materials.append(mat)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Create a cube with specified size in Blender.")
    parser.add_argument('-l', '--length', type=float, help="Length of the cube.", default=2.0)
    parser.add_argument('-w', '--width', type=float, help="Width of the cube.", default=2.0)
    parser.add_argument('-h', '--height', type=float, help="Height of the cube.", default=2.0)

    
    # Extract arguments after '--'
    if "--" in sys.argv:
        args, __ = parser.parse_known_args(sys.argv[sys.argv.index("--") + 1:])
    else:
        # Default args if not running from CLI
        args = parser.parse_args([])
    
    return args

def main():
    # Conditionally parse arguments if script is run from CLI with '--'
    logging.info('wind')
    if "--" in sys.argv:
        args = parse_arguments()
        # Create a cube with the specified dimensions
        create_cube(args.length, args.width, args.height)
    else:
        # Default behavior for direct execution in Blender
        create_cube()
    
    # Set the cube colour
    set_cube_colour()

    render.setup_scene()
    render.render_image(os.path.join(os.environ['BLENDER_OUTPUT'], "test_wind.png"))
if __name__ == "__main__":
    main()
