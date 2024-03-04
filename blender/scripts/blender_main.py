
import jsonpickle
from blender_object import *
import subprocess

def create_blender_json(num_zones, heights, loads):
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, HeightZone(h=heights[i], load=loads[i], position=i).to_dict())

    
    json_str = jsonpickle.encode(json_str)
    
    return json_str

json_str = create_blender_json(3, [2,2,2], [25,40,20])
print(json_str)

data = jsonpickle.decode(json_str)
print(data)
print(data[0]['h'])
#command = f"blender --background --python .\blender\scripts\wind_cube.py -- 1 {json_str}"
#result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#print(f"ran successfully:", result.stdout.decode())