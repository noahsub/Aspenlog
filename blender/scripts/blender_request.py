
import sys
sys.path.append('C:\\Users\\Alastair\\Dev\\SEEDA\\blender\\scripts')
sys.path.append('C:\\Users\\Alastair\\Dev\\SEEDA\\blender\\objects')
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import json
from blender_object import *
import jsonpickle
# Check for args
if len(sys.argv) < 3:
    print("Usage: blender --background --python blender_request.py -- id '<json_string>'")
    sys.exit(1)

# last argument is JSON string
#json_str = sys.argv[-1]
id = int(sys.argv[-1])
def create_blender_json(num_zones, heights, loads):
    json_str = [Arrow()]
    for i in range(num_zones):
        json_str.insert(0, HeightZone(h=heights[i], load=loads[i], position=i).to_dict())

    
    json_str = jsonpickle.encode(json_str)
    
    return json_str

#json_str = create_blender_json(3, [2,2,2], [25,40,20])
#print(json_str)

#data = jsonpickle.decode(json_str)
def run_blender_script(script_path):
    blender_path = os.environ['BLENDER'] 
    args = ['--background', '--python', script_path, '--', id, json_str ]

    # Combine the Blender path and arguments
    command = [blender_path] + args
    print(command)
    # Run the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{script_path} ran successfully:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:", e.stderr.decode())

# Paths to the scripts
scripts = ["./seismic_cube.py", "./wind_cube.py"]

# Run the scripts in parallel
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(run_blender_script, scripts)
