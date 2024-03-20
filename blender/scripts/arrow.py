########################################################################################################################
# arrow.py
# This file contains the code to create an arrow in Blender.
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
import bmesh
import math


########################################################################################################################
# FUNCTIONS
########################################################################################################################


def create_arrow(
    length=0.2,
    width=0.2,
    height=0.2,
    loc_x=3,
    loc_y=3,
    rot_x=math.pi / 2,
    rot_y=0,
    rot_z=math.pi,
):
    """
    Create an arrow in Blender.
    :param length: The length of the arrow.
    :param width: The width of the arrow.
    :param height: The height of the arrow.
    :param loc_x: The x location of the arrow.
    :param loc_y: The y location of the arrow.
    :param rot_x: The x rotation of the arrow.
    :param rot_y: The y rotation of the arrow.
    :param rot_z: The z rotation of the arrow.
    :return: None
    """
    cone_x = length
    cone_y = width
    cone_z = height * 3

    # Add a cone and cylinder
    bpy.ops.mesh.primitive_cone_add(enter_editmode=False, location=(0, 0, cone_z))
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, 0, -cone_z))
    # Get the active objects
    cone = bpy.data.objects["Cone"]
    cyl = bpy.data.objects["Cylinder"]
    # Scale the cone to desired dimensions
    cone.scale.x = cone_x
    cone.scale.y = cone_y
    cone.scale.z = cone_z

    cyl.scale.x = cone_x * 0.2
    cyl.scale.y = cone_y * 0.2
    cyl.scale.z = cone_z * 1.5

    # join the shapes
    cone.select_set(True)
    cyl.select_set(True)
    bpy.ops.object.join()
    arrow = bpy.context.active_object
    arrow.location[0] = loc_x
    arrow.location[1] = loc_y
    arrow.location[2] = height

    arrow.rotation_euler[0] = rot_x
    # y
    arrow.rotation_euler[1] = rot_y
    # z
    arrow.rotation_euler[2] = rot_z
    bpy.ops.object.select_all(action="DESELECT")
