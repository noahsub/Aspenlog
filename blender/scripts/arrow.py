import bpy
import bmesh
def create_arrow(length=2.0, width=2.0, height=2.0):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    cone_x = length 
    cone_y = width 
    cone_z = height*3

    # Add a cone and cylinder
    bpy.ops.mesh.primitive_cone_add(enter_editmode=False, location=(0, 0, cone_z))
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, 0, -cone_z))
    # Get the active objects
    cone = bpy.data.objects['Cone']
    cyl = bpy.data.objects['Cylinder']
    # Scale the cone to desired dimensions
    cone.scale.x = cone_x
    cone.scale.y = cone_y
    cone.scale.z = cone_z

    cyl.scale.x = cone_x * 0.2
    cyl.scale.y = cone_y *0.2
    cyl.scale.z = cone_z *1.5

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    # Apply the scaling transformation
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.select_all(action='SELECT')
    # join the shapes
    bpy.ops.object.join()
    # Enter edit mode to modify the cube
    #bpy.ops.object.editmode_toggle()
