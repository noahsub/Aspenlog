from backend.Constants.wind_constants import GUST_FACTOR


class WindFactor:
    ct: float
    ce: float
    cei: float
    cg: float

    def __init__(self, ct: float, ce: float, cei: float):
        self.ct = ct
        self.ce = ce
        self.cei = cei
        self.cg = GUST_FACTOR

    def __str__(self):
        return (f"ct: {self.ct}\n"
                f"ce: {self.ce}\n"
                f"cei: {self.cei}\n"
                f"cg: {self.cg}")


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

    def __str__(self):
        return (f"pi_pos: {self.pi_pos}\n"
                f"pi_neg: {self.pi_neg}\n"
                f"pe_pos: {self.pe_pos}\n"
                f"pe_neg: {self.pe_neg}")


class Zone:
    name: str
    num: int
    pressure: WindPressure
    wind_load: float

    def __init__(self, name: str, num: int, pressure: WindPressure, wind_load: float = None):
        self.name = name
        self.num = num
        self.pressure = pressure
        self.wind_load = None

    def __str__(self):
        return (f"name: {self.name}\n"
                f"num: {self.num}\n"
                f"pressure: {self.pressure}\n"
                f"wind_load: {self.wind_load}")


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

    def __str__(self):
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))
        pressure_str = '\n  ' + '\n  '.join(str(self.pressure).split('\n'))

        zones_str = '\n'
        for zone in self.zones:
            zones_str += f"  zone {zone.num}\n"
            zone_lst = str(zone).split('\n')
            for i in zone_lst:
                zones_str += f"    {i.lstrip(', ')}\n"
        zones_str = zones_str[:-1]

        return (f"factor: {factor_str}\n"
                f"pressure: {pressure_str}\n"
                f"zones: {zones_str}")
