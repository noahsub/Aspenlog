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
import math


########################################################################################################################
# FUNCTIONS
########################################################################################################################


def set_camera_position(
    max_height, camera, focal_length=50, sensor_height=24, extra_space_factor=1.1
):
    """
    Adjust the camera position to ensure the target object is fully visible in frame.

    Args:
    - target_object: The object you want to frame.
    - camera: The camera object.
    - focal_length: The focal length of the camera in mm. Default is 50mm.
    - sensor_height: The sensor height of the camera in mm. Default for full-frame is 24mm.
    - extra_space_factor: A factor to add some extra space around the target object. Default is 1.1 (10% extra space).

    :param max_height: The maximum height of the object in the scene.
    :param camera: The camera object.
    :param focal_length: The focal length of the camera in mm. Default is 50mm.
    :param sensor_height: The sensor height of the camera in mm. Default for full-frame is 24mm.
    :param extra_space_factor: A factor to add some extra space around the target object. Default is 1.1 (10% extra space).
    :return: None
    """
    # Calculate the vertical field of view (vFoV)
    vFoV = 2 * math.atan(sensor_height / (2 * focal_length))

    # Calculate the distance required to fit the object in view
    distance = (max_height / 2) / math.tan(vFoV / 2) * extra_space_factor

    # Update camera data
    camera.data.lens = focal_length
    camera.data.sensor_height = sensor_height

    # Position the camera - Adjust as necessary for your scene
    camera.location.x = distance
    camera.location.y = -distance
    camera.location.z = (max_height / 2) - 0.1 * max_height

    # Point the camera to look at the target object
    # Rotational Coordinates
    # x
    camera.rotation_euler[0] = math.pi / 2
    # y
    camera.rotation_euler[1] = 0
    # z
    camera.rotation_euler[2] = math.pi / 4


####
def hex_to_rgb(value):
    """
    Converts a hex color to an RGB tuple normalized to [0, 1].

    :param value: The hex color value.
    :return: An RGB tuple normalized to [0, 1].
    """
    value = value.lstrip("#")
    lv = len(value)
    rgb = [int(value[i : i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3)]
    return (rgb[0], rgb[1], rgb[2])


def setup_scene(max_height):
    """
    Set up the scene for rendering.
    :param max_height: The maximum height of the object in the scene.
    :return: None
    """
    # Set render resolution
    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 720
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.film_transparent = True
    hex_color = "#f7f4ef"

    # Convert hex to RGB
    # rgb_color = hex_to_rgb(hex_color)
    # (0.969, 0.957, 0.937)
    # Set the background color using the converted RGB values

    # bpy.context.scene.world.color = rgb_color
    # Check if camera exists
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(7.0, -7.0, 7.0), rotation=(63.4, 0.0, 45.0))
    camera = bpy.data.objects.get("Camera")
    bpy.context.scene.camera = camera

    ######
    focal_length = camera.data.lens
    sensor_height = camera.data.sensor_height
    set_camera_position(max_height, camera, focal_length=50, sensor_height=24)

    # light
    if "Light" not in bpy.data.objects:
        bpy.ops.object.light_add(type="POINT", location=(0, 0, 10))
    light = bpy.data.objects.get("Light")
    light.data.energy = 1000  # Adjust light intensity

    # adjust light position
    light.location[0] = 3
    light.location[1] = -1.9
    # light.visible_shadow = False
    # bpy.context.scene.eevee.use_shadow = False


# def render_image(output_path):
#     # Set the output path
#     bpy.context.scene.render.filepath = output_path
#
#     # Set render engine to Cycles for better quality (optional)
#
#     #bpy.context.scene.render.engine = 'CYCLES'
#     # easier to render but no background choices
#     bpy.context.scene.render.engine = 'BLENDER_EEVEE'
#
#     # Render the scene
#     bpy.ops.render.render(write_still=True)


def render_image(output_path):
    """
    Render the image and save it to the output path.
    :param output_path: The output path for the rendered image.
    :return: None
    """
    # Set the output path
    bpy.context.scene.render.filepath = output_path

    # Set render engine to Cycles for better quality (optional)
    bpy.context.scene.render.engine = (
        "CYCLES"  # or 'BLENDER_EEVEE' for faster rendering
    )
    # bpy.context.scene.render.use_freestyle=True
    # bpy.context.scene.render.line_thickness = 0.5
    # bpy.context.scene.render.line_thickness_mode = "RELATIVE"
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cycles_preferences.refresh_devices()
    devices = list(cycles_preferences.devices)

    cuda_devices = [x for x in devices if str(x.type) == "CUDA"]
    cpu_devices = [x for x in devices if str(x.type) == "CPU"]

    # reduce for less vram
    # bpy.context.scene.render.simplify_subdivision_render =10

    if len(cuda_devices) > 0:

        bpy.context.scene.cycles.texture_limit_render = "128"

        # default 4096
        bpy.context.scene.cycles.samples = 10

        bpy.context.scene.cycles.adaptive_threshold = 1

        bpy.context.scene.cycles.use_auto_tile = True
        # bpy.context.scene.cycles.debug_use_compact_bvh = True

        bpy.context.scene.cycles.use_denoising = False

        # Lower = slightly less ram, default 2048, 64 seems good, 512 is faster with a bit more mem
        bpy.context.scene.cycles.tile_size = 512

        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = (
            "CUDA"
        )
        for device in cuda_devices:
            print(f"Using {device} for rendering")
            device.use = True
        bpy.context.scene.cycles.device = "GPU"
    else:
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
        print("No CUDA devices available, falling back to CPU EEVEE rendering")

    # Render the scene
    bpy.ops.render.render(write_still=True)
