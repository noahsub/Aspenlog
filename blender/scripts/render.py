import bpy

def setup_scene():
    # Set render resolution
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100

    # Check if camera exists, if not, create one
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(7.0, -7.0, 7.0), rotation=(63.4, 0.0, 45.0))
    camera = bpy.data.objects.get("Camera")
    bpy.context.scene.camera = camera

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
    


