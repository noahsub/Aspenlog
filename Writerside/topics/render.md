# Blender Rendering

## File: render.py

This file contains the code to set up the scene and render the image in Blender.
The code creates a camera and light and places them in a position where the camera can view the whole
structure. The render process is optimized to reduce memory usage and will utilize a GPU render if one is
available.