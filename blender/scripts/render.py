import bpy
import math 

def set_camera_position(max_height, camera, focal_length=50, sensor_height=24, extra_space_factor=1.1):
    """
    Adjust the camera position to ensure the target object is fully visible in frame.
    
    Args:
    - target_object: The object you want to frame.
    - camera: The camera object.
    - focal_length: The focal length of the camera in mm. Default is 50mm.
    - sensor_height: The sensor height of the camera in mm. Default for full-frame is 24mm.
    - extra_space_factor: A factor to add some extra space around the target object. Default is 1.1 (10% extra space).
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
    camera.location.z = (max_height / 2)-0.1*max_height
    
    # Point the camera to look at the target object
    # Rotational Coordinates
    # x 
    camera.rotation_euler[0] = math.pi/2
    # y
    camera.rotation_euler[1] = 0
    # z
    camera.rotation_euler[2] = math.pi/4

####
def setup_scene(max_height):
    # Set render resolution
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100

    # Check if camera exists, if not, create one
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(7.0, -7.0, 7.0), rotation=(63.4, 0.0, 45.0))
    camera = bpy.data.objects.get("Camera")
    bpy.context.scene.camera = camera

    ######
    focal_length = camera.data.lens
    sensor_height = camera.data.sensor_height
    set_camera_position(max_height, camera, focal_length=50, sensor_height=24)

    # Ensure there is a light in the scene
    if "Light" not in bpy.data.objects:
        bpy.ops.object.light_add(type='POINT', location=(0, 0, 10))
    light = bpy.data.objects.get("Light")
    light.data.energy = 1000  # Adjust light intensity

def render_image(output_path):
    # Set the output path
    bpy.context.scene.render.filepath = output_path

    # Set render engine to Cycles for better quality (optional)
    bpy.context.scene.render.engine = 'CYCLES'

    # Render the scene
    bpy.ops.render.render(write_still=True)
    


