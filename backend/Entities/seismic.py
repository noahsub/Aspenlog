class SeismicFactor:
    ar: float
    rp: float
    cp: float

    def __init__(self, ar: float = 1, rp: float = 2.5, cp: float = 1):
        self.ar = ar
        self.rp = rp
        self.cp = cp

class SeismicLoad:
    factor: SeismicFactor