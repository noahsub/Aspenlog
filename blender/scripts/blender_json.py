import json
import objects
def create_blocks(num_blocks):
    zones = []
    for i in range(num_blocks):
        zone = objects.blender_object.HeightZone(None, None, None, i)
        zones.append(zone)