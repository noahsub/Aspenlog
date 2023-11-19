class WindFactor:
    ct: float
    ce: float
    cei: float
    cg: float

    def __init__(self, ct: float, ce: float, cei: float, cg: float):
        self.ct = ct
        self.ce = ce
        self.cei = cei
        self.cg = cg


class WindPressure:
    pi_pos: float
    pi_neg: float
    pe_pos: float
    pe_neg: float

    def __init__(self, pi_pos: float = None, pi_neg: float = None, pe_pos: float = None, pe_neg: float = None):
        self.pi_pos = pi_pos
        self.pi_neg = pi_neg
        self.pe_pos = pe_pos
        self.pe_neg = pe_neg


class Zone:
    name: str
    num: int
    pressure: WindPressure
    wind_load: float

    def __init__(self, name: str, num: int, pressure: WindPressure, wind_load: float = None):
        self.name = name
        self.num = num
        self.pressure = pressure


class WindLoad:
    factor: WindFactor
    pressure: WindPressure
    zones: set[Zone]

    def __init__(self, factor: WindFactor, pressure: WindPressure):
        self.factor = factor
        self.pressure = pressure
        self.zones = {
            Zone('roof_interior', 1, WindPressure()),
            Zone('roof_edge', 2, WindPressure()),
            Zone('roof_corner', 3, WindPressure()),
            Zone('wall_centre', 4, WindPressure()),
            Zone('wall_corner', 5, WindPressure())
        }

    def get_zone(self, key):
        if type(key) == str:
            for zone in self.zones:
                if zone.name == key:
                    return zone
        elif type(key) == int:
            for zone in self.zones:
                if zone.num == key:
                    return zone
