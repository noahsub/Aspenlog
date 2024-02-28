import sys
import json
import objects

# Check for args
if len(sys.argv) < 5:
    print("Usage: blender --background --python script.py -- '<json_string>'")
    sys.exit(1)

# last argument is JSON string
json_str = sys.argv[-1]
height = float(sys.argv[-4])
width = float(sys.argv[-3])
length = float(sys.argv[-2])

try:
    # Parse the JSON string
    data = json.loads(json_str)
    
    # Now you can use the data object as needed, for example:
    print("Data received:", data)
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)
    sys.exit(1)



