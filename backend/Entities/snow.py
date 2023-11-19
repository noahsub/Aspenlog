class SnowFactor:
    cs: float
    ca: float
    cw: float
    cb: float

    def __init__(self, cs: float, ca: float, cw: float, cb: float):
        self.cs = cs
        self.ca = ca
        self.cw = cw
        self.cb = cb


class SnowLoad:
    factor: SnowFactor
    s: float

    def __init__(self, factor: SnowFactor, s: float):
        self.factor = factor
        self.s = s
