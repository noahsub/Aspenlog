import bpy
import sys
import render
import os
import math
import bmesh

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
    bpy.ops.object.modifier_add(type="EDGE_SPLIT")
    set_cube_colour(cube, rgba=(r, g, 0.0, 1.0), text=False)
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
    
    if angle_degrees < 90 and angle_degrees!= 0:

        base_width = 2.0  # Length of the square base sides
        half_base = base_width / 2
        angle_radians = math.radians(angle_degrees)
        triangle_height = math.tan(angle_radians) * half_base
        print("Tri heightL", triangle_height, "\tTotal:", total_height)
        if "Cube" in bpy.data.objects:
            # Deleting Default Cube
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Cube'].select_set(True)
            bpy.ops.object.delete()

        # add cylinder
        bpy.ops.mesh.primitive_cylinder_add(vertices=3)
        bpy.data.objects["Cylinder"].rotation_euler[0] = math.pi/2
        bpy.data.objects["Cylinder"].scale[1] = triangle_height

        bpy.data.objects["Cylinder"].location[2] = total_height-triangle_height/2
        #bpy.context.scene.objects.link(object)
        obj = bpy.context.view_layer.objects.active
        if obj.type == 'MESH':
            # Switch to Object Mode (required to make changes to mesh data)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            
            for face in bm.faces:
                face.select = False
            bm.faces[1].select = True
            #VALUE = 5
            bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context=None, TRANSFORM_OT_translate={"value":(0,0,-(total_height-triangle_height))})
            #bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":total_height-triangle_height})
            #bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":float(total_height-triangle_height)})
            
            # Switch back to Object Mode if necessary
            bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Angle out of Bounds, Generating default")

        bpy.ops.mesh.primitive_cube_add(scale=(2,2,total_height))
    obj = bpy.context.view_layer.objects.active
    set_cube_colour(obj, rgba=(0.7, 0.5, 0.5, 1.0))

def set_cube_colour(cube, rgba=(1.0, 0.0, 0.0, 1.0), text=False, emit=False):

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

    #principled_bsdf.inputs[26].default_value = rgba
    #principled_bsdf.inputs[27].default_value = 0.5
    if emit:
        principled_bsdf.inputs[26].default_value = rgba
        principled_bsdf.inputs[27].default_value = 0.5

    # Assign the material to the object
    if cube.data.materials:
        # If the object already has material slots
        cube.data.materials[0] = mat
    else:
        # If the object has no material slots
        cube.data.materials.append(mat)


def create_axis(radius=0.05, depth=1, location=(0, -3, 2) ):
    bpy.ops.object.select_all(action='DESELECT')
    # y
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1, enter_editmode=False, location=(0, depth/2, 0), rotation=(math.pi/2, 0 , math.pi))
    y = bpy.context.active_object
    y.name = 'yaxis'
    set_cube_colour(y, rgba=(0.0,1.0,0.0,1.0))
    
    # z
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1, enter_editmode=False, location=(0, 0, depth/2), rotation=(0, 0 , math.pi/2))
    z = bpy.context.active_object
    z.name = 'zaxis'
    set_cube_colour(z, rgba=(0.0,0.0,1.0,1.0))
    
    #

    # x
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1, enter_editmode=False, location=(depth/2, 0, 0), rotation=(0, math.pi/2 , 0))
    x = bpy.context.active_object
    x.name = 'xaxis'
    set_cube_colour(x, rgba=(1.0,0.0,0.0,1.0))
   
    
    obj = bpy.data.objects['yaxis']
    obj.select_set(True)
    obj = bpy.data.objects['zaxis']
    obj.select_set(True)
    obj = bpy.data.objects['xaxis']
    obj.select_set(True)
    
    #bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.join()
    axis = bpy.context.active_object
    axis.name='Axis'
    axis.location = location
    
    # add labels
    obj=add_axis_text('Y', location=(location[0], location[1]+depth, location[2]))
    obj.name = 'ylabel'
    set_cube_colour(obj, rgba=(0.0,1.0,0.0,1.0))
    
    obj=add_axis_text('Z', location=(location[0], location[1], location[2]+depth))
    obj.name = 'zlabel'
    set_cube_colour(obj, rgba=(0.0,0.0,1.0,1.0))
    
    obj=add_axis_text('X', location=(location[0]+depth, location[1]-0.3, location[2]))
    obj.name = 'xlabel'
    set_cube_colour(obj, rgba=(1.0,0.0,0.0,1.0))
    
def add_axis_text(axis, location, scale=(0.3, 0.3, 0.3)):


    font_curve = bpy.data.curves.new(type="FONT", name="numberPlate")

    font_curve.body = str(axis)
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)

    # -- Set scale and location
    obj.location = location
    obj.rotation_euler = (math.pi/2, 0, math.pi/2)
    obj.scale = scale
     # Link the object to the active collection in the current view layer
    bpy.context.view_layer.active_layer_collection.collection.objects.link(obj)
    return obj

def max_height_check(height_list, limit=15 ):
    total_height = sum(height_list)
    output_heights = []
    if total_height > limit:
        map_factor = limit/total_height
        for height in height_list:
            output_heights.append(height*map_factor)
    else:
        output_heights = height_list
    return output_heights
