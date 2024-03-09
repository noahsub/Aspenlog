import bpy
import sys
import render
import os


def create_wind_cube(length=2.0, width=2.0, height=2.0, position=0, r=1.0, g=1.0):  

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
    cube =bpy.context.active_object
    cube.name="Base Cube"
    set_cube_colour(cube, rgba=(r, 0.0, 0.0, 1.0))
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(cube_x/2+length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(-cube_x/2-length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(cube_x/2+length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(-cube_x/2-length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.join()
    cube = bpy.context.active_object
    set_cube_colour(cube, rgba=(r, g, 0.0, 1.0))
    bpy.ops.object.select_all(action='DESELECT')

def create_seismic_cube(length=2.0, width=2.0, height=2.0, position=0):

    cube_x = length 
    cube_y = width 
    cube_z = height

    # Add a cube
    bpy.ops.mesh.primitive_cube_add(scale=(cube_x, cube_y, cube_z), size=1, enter_editmode=False, location=(0, 0, position*cube_z))

    # Get the active object (the cube we just added)
    cube = bpy.context.active_object
    return cube

def set_cube_colour(cube, rgba=(1.0, 0.0, 0.0, 1.0)):

    # Create a new material
    mat = bpy.data.materials.new(name="CustomMaterial")

    # Enable 'Use nodes':
    mat.use_nodes = True

    # Access the principled BSDF, the default shader for new materials
    principled_bsdf = mat.node_tree.nodes.get('Principled BSDF')

    # Set the color - in RGBA format, from 0.0 to 1.0
    # red
    principled_bsdf.inputs['Base Color'].default_value = rgba # Red

    # Assign the material to the object
    if cube.data.materials:
        # If the object already has material slots
        cube.data.materials[0] = mat
    else:
        # If the object has no material slots
        cube.data.materials.append(mat)