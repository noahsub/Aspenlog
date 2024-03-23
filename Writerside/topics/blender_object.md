# Wind, Seismic, and Arrow objects

## File: blender_object.py

This file contains code to create object classes for wind and seismic zones as well as the arrow.
The zones are called by the frontend API in order to pass the data in a JSON string. The objects contain
a to_dict() method in order to properly be encoded in to a JSON string.

### Wind Zone
The wind zone object stores:
- Wind Loads: wall_centre_pos, wall_centre_neg, wall_corner_pos, wall_corner_neg 
- Height of the height zone: h 
- Position in the in JSON string: position

### Seismic Zone
The seismic zone object stores:
- Seismic Load: load
- Height of the height zone: h
- Position in the in JSON string: position

### Arrow
The arrow object stores:
- Yaw: yaw
- Position in the in JSON string: position