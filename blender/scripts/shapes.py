import bpy
import sys
import render
import os
import math

def create_wind_cube(length=2.0, width=2.0, height=2.0, position=0, r=1.0, g=1.0):  

    cube_x = length * 0.9
    cube_y = width * 0.9
    cube_z = height 
    
    block_z = position
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
    set_cube_colour(cube, rgba=(1.0, 1.0, 1.0, 1.0), text=True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(cube_x/2+length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(-cube_x/2-length*0.05, cube_y/2+width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(cube_x/2+length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True,  location=(-cube_x/2-length*0.05, -cube_y/2-width*0.05, block_z), scale=(0.1,0.1,cube_z/2))
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.join()
    cube = bpy.context.active_object
    set_cube_colour(cube, rgba=(r, g, 0.0, 1.0), text=True)
    bpy.ops.object.select_all(action='DESELECT')

def create_seismic_cube(length=2.0, width=2.0, height=2.0, position=0):

    cube_x = length 
    cube_y = width 
    cube_z = height

    # Add a cube
    bpy.ops.mesh.primitive_cube_add(scale=(cube_x, cube_y, cube_z), size=1, enter_editmode=False, location=(0, 0, position))

    # Get the active object (the cube we just added)
    cube = bpy.context.active_object
    return cube

def create_simple_cube(angle_degrees=45, total_height=20):
    
    if angle_degrees < 90:

        base_width = 2.0  # Length of the square base sides
        half_base = base_width / 2
        angle_radians = math.radians(angle_degrees)
        triangle_height = math.tan(angle_radians) * half_base

        # add cylinder
        bpy.ops.mesh.primitive_cylinder_add(vertices=3)
        bpy.data.objects["Cylinder"].rotation_euler[0] = math.pi/2
        bpy.data.objects["Cylinder"].scale[1] = triangle_height

        bpy.data.objects["Cylinder"].location[2] = total_height-triangle_height

        obj = bpy.context.active_object
        if obj.type == 'MESH':
            # Switch to Object Mode (required to make changes to mesh data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Retrieve the mesh data of the object
            mesh = obj.data
            
            # Assume we want to select the face with index 0
            face_index = 1
            
            # Deselect all faces
            for face in mesh.polygons:
                face.select = False
            
            # Select the face with the specified index
            mesh.polygons[face_index].select = True
            
            # Update the mesh to apply the selection
            obj.update_from_editmode()
            
            # Switch to Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Make sure we're using face selection mode
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            
            # Extrude the selected face
            #bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value"=total_height})
            bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":float(total_height)})

            # Apply the shrink/fatten transformation with the specified value to the extruded faces
            #bpy.ops.transform.shrink_fatten(value=total_height, use_even_offset=True)
            
            # Switch back to Object Mode if necessary
            bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Angle out of Bounds, Generating default")

        bpy.ops.mesh.primitive_cube_add(scale=(2,2,total_height))

def set_cube_colour(cube, rgba=(1.0, 0.0, 0.0, 1.0), text=False):

    # Create a new material
    mat = bpy.data.materials.new(name="CustomMaterial")
    if text:
        mat.shadow_method = 'NONE'
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