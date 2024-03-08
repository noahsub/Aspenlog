import bpy
import bmesh
import math
def create_arrow(length=0.2, width=0.2, height=0.2):
    

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


    # join the shapes
    cone.select_set(True)
    cyl.select_set(True)
    bpy.ops.object.join()
    arrow = bpy.context.active_object
    arrow.location[0] = 2*length
    arrow.location[1] = 2*width
    arrow.location[2] = height

    arrow.rotation_euler[0] = math.pi/2
    # y
    arrow.rotation_euler[1] = 0
    # z
    arrow.rotation_euler[2] = math.pi/4
