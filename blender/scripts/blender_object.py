########################################################################################################################
# blender_object.py
# This file contains the code to create the object classes for the wind and seismic zones and the arrow.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: [https://github.com/alastairsim]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from typing import Optional, Tuple


########################################################################################################################
# OBJECT CLASSES
########################################################################################################################

class WindZone:
    """
    This class is used to store the height zone information.
    """

    def __init__(self, wall_centre_pos: float, wall_centre_neg: float, wall_corner_pos: float, wall_corner_neg: float,
                 h: Optional[float] = None, position: Optional[int] = None):
        """
        Initialize the WindZone object.
        :param wall_centre_pos: The positive wind load at the centre of the wall.
        :param wall_centre_neg: The negative wind load at the centre of the wall.
        :param wall_corner_pos: The positive wind load at the corner of the wall.
        :param wall_corner_neg: The negative wind load at the corner of the wall.
        :param h: The height of the wind zone.
        :param position: The position of the wind zone.
        """
        self.h = h
        self.wall_centre_pos = wall_centre_pos
        self.wall_centre_neg = wall_centre_neg
        self.wall_corner_pos = wall_corner_pos
        self.wall_corner_neg = wall_corner_neg
        self.position = position

    def to_dict(self):
        """
        Convert the WindZone object to a dictionary.
        :return: A dictionary containing the WindZone object.
        """
        return {"h": self.h, "wall_centre_pos": self.wall_centre_pos, "wall_centre_neg": self.wall_centre_neg,
                "wall_corner_pos": self.wall_corner_pos, "wall_corner_neg": self.wall_corner_neg,
                "position": self.position}


class SeismicZone:
    """
    This class is used to store the height zone information.
    """

    def __init__(self, h: Optional[float] = None, load: Optional[float] = None, position: Optional[int] = None):
        """
        Initialize the SeismicZone object.
        :param h: The height of the seismic zone.
        :param load: The seismic load of the seismic zone.
        :param position: The position of the seismic zone.
        """
        # tuple takes pos_uls and neg_uls in that order
        self.h = h
        self.load = load
        self.position = position

    def to_dict(self):
        """
        Convert the SeismicZone object to a dictionary.
        :return: A dictionary containing the SeismicZone object.
        """
        return {"h": self.h, "load": self.load, "position": self.position}


class Arrow:
    """
    This class is used to store the arrow object.
    """

    def __init__(self, yaw: Optional[float] = None, position: Optional[int] = None):
        """
        Initialize the Arrow object.
        :param yaw: The yaw of the arrow.
        :param position: The position of the arrow.
        """
        self.yaw = yaw
        self.position = position

    def to_dict(self):
        """
        Convert the Arrow object to a dictionary.
        :return: A dictionary containing the Arrow object.
        """
        return {"yaw": self.yaw, "position": self.position}
