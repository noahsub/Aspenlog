class SeismicFactor:
    ar: float
    rp: float
    cp: float

    def __init__(self, ar: float = 1, rp: float = 2.5, cp: float = 1):
        self.ar = ar
        self.rp = rp
        self.cp = cp

    def __str__(self):
        return (f"ar: {self.ar}\n"
                f"rp: {self.rp}\n"
                f"cp: {self.cp}")


class SeismicLoad:
    factor: SeismicFactor
    ax: float
    sp: float
    vp: float
    vp_snow: float

    def __init__(self, factor: SeismicFactor, ax: float, sp: float, vp: float, vp_snow: float):
        self.factor = factor
        self.ax = ax
        self.sp = sp
        self.vp = vp
        self.vp_snow = vp_snow

    def __str__(self):
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))

        return (f"factor: {factor_str}\n"
                f"ax: {self.ax}\n"
                f"sp: {self.sp}\n"
                f"vp: {self.vp}\n"
                f"vp_snow: {self.vp_snow}")


