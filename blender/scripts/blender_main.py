
import jsonpickle
from blender_object import *
import subprocess
import os
req_file = __file__
req_file = os.path.join(os.path.dirname(req_file), 'blender_request.py')

def create_blender_json(num_zones, heights, loads):
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, WindZone(h=heights[i], load=loads[i], position=i).to_dict())

    
    json_str = jsonpickle.encode(json_str)
    
    return json_str

json_str = create_blender_json(3, [2,2,2], [25,40,20])
command = ['blender', '--background', '--python', req_file, '--', '2', json_str]
print(command)
result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(f"ran successfully:", result.stdout.decode())