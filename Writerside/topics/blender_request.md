# Running Blender in the Background

## File: blender_request.py

This file contains code called by the frontend API to run a blender process in the background for a given json_str.

The subprocess command is:


`blender --background --python <script_name> -- id <json_string>`

For example:


`blender --background --python wind_cube.py -- id '[{h:2, load:1.22}]'`