class WindFactor:
    ct: float
    ce: float
    cg: float

    def __init__(self, ct: float, ce: float, cg: float):
        self.ct = ct
        self.ce = ce
        self.cg = cg


class WindPressure:
    pi_pos: float
    pi_neg: float
    pe_pos: float
    pe_neg: float

    def __init__(self, pi_pos: float, pi_neg: float, pe_pos: float, pe_neg: float):
        self.pi_pos = pi_pos
        self.pi_neg = pi_neg
        self.pe_pos = pe_pos
        self.pe_neg = pe_neg


class WindLoad:
    factor: WindFactor
    pressure: WindPressure

    def __init__(self, factor: WindFactor, pressure: WindPressure):
        self.factor = factor
        self.pressure = pressure
