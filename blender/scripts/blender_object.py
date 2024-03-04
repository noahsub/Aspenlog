from typing import Optional, Tuple

class HeightZone:
    """
    This class is used to store the height zone information.
    """
    def __init__(self, h: Optional[float] = None, load: Optional[float] = None, position: Optional[int] = None):
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