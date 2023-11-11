class Dimensions:
    height: float
    width: float

    def __init__(self, height: float, width: float):
        self.height = height
        self.width = width


class Cladding:
    c_top: float
    c_bot: float

    def __init__(self, c_top: float, c_bot: float):
        self.c_top = c_top
        self.c_bot = c_bot


class Roof:
    w_roof: float
    l_roof: float
    slope: float


class Building:
    dimensions: Dimensions
    cladding: Cladding
    roof: Roof
    hz_num: int
    h_opening: float

    def __init__(self, dimensions: Dimensions, cladding: Cladding, roof: Roof, hz_num: int, h_opening: float):
        self.dimensions = dimensions
        self.cladding = cladding
        self.roof = roof
        self.hz_num = hz_num
        self.h_opening = h_opening





