from backend.Constants.snow_constants import ACCUMULATION_FACTOR


class SnowFactor:
    cs: float
    ca: float
    cw: float
    cb: float

    def __init__(self, cs: float, cw: float, cb: float):
        self.cs = cs
        self.ca = ACCUMULATION_FACTOR
        self.cw = cw
        self.cb = cb

    def __str__(self):
        return (f"cs: {self.cs}\n"
                f"ca: {self.ca}\n"
                f"cw: {self.cw}\n"
                f"cb: {self.cb}")


class SnowLoad:
    factor: SnowFactor
    s: float

    def __init__(self, factor: SnowFactor, s: float):
        self.factor = factor
        self.s = s

    def __str__(self):
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))

        return (f"factor: {factor_str}\n"
                f"s: {self.s}")
