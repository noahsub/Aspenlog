from typing import Optional, Tuple

class WindZone:
    """
    This class is used to store the height zone information.
    """
    def __init__(self, wall_centre_pos: float, wall_centre_neg: float, wall_corner_pos: float, wall_corner_neg: float, h: Optional[float] = None, position: Optional[int] = None):
        self.h = h
        self.wall_centre_pos = wall_centre_pos
        self.wall_centre_neg = wall_centre_neg
        self.wall_corner_pos = wall_corner_pos
        self.wall_corner_neg = wall_corner_neg
        self.position = position

    def to_dict(self):
        return {"h": self.h, "load": self.load, "position": self.position}

class SeismicZone:
    """
    This class is used to store the height zone information.
    """
    def __init__(self, h: Optional[float] = None, load: Optional[float] = None, position: Optional[int] = None):
        # tuple takes pos_uls and neg_uls in that order
        self.h = h
        self.load = load
        self.position = position

    def to_dict(self):
        return {"h": self.h, "load": self.load, "position": self.position}
    
class Arrow:
    """
    This class is used to store the arrow object.
    """
    def __init__(self, yaw: Optional[float] = None, position: Optional[int] = None):
        self.yaw = yaw
        self.position = position

    def to_dict(self):
        return {"yaw": self.yaw, "position": self.position}