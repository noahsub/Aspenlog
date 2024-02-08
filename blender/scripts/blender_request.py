
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

def run_blender_script(script_path):
    blender_path = os.environ['BLENDER'] 
    args = ['--background', '--python', script_path]

    # Combine the Blender path and arguments
    command = [blender_path] + args

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
