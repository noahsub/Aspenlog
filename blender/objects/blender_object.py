from typing import Optional, Tuple

class HeightZone:
    """
    This class is used to store the height zone information.
    """
    def __init__(self, h: Optional[float] = None, w: Optional[float] = None, l: Optional[float] = None, position: Optional[int] = None):
        self.h = h
        self.w = w
        self.l = l
        self.position = position

class Arrow:
    """
    This class is used to store the arrow object.
    """
    def __init__(self, h: Optional[float] = None, w: Optional[float] = None, l: Optional[float] = None, position: Optional[int] = None):
        self.h = h
        self.w = w
        self.l = l
        self.position = position
