import math


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
    wall_slope: int

    def __init__(self, w_roof: float, l_roof: float, slope: float):
        self.w_roof = w_roof
        self.l_roof = l_roof
        self.slope = slope
        if 30 <= slope <= 70:
            self.wall_slope = 1
        else:
            self.wall_slope = 0


class HeightZone:
    zone_num: int
    elevation: float

    def __init__(self, zone_num: int, elevation: float = 0):
        self.zone_num = zone_num
        self.elevation = elevation

    def __str__(self):
        return f"hz{self.zone_num}: {self.elevation}m"


class Building:
    dimensions: Dimensions
    cladding: Cladding
    roof: Roof
    hz_num: int
    h_opening: float
    height_zones: list[HeightZone]

    def __init__(self, dimensions: Dimensions, cladding: Cladding, roof: Roof, h_opening: float):
        self.dimensions = dimensions
        self.cladding = cladding
        self.roof = roof
        self.h_opening = h_opening

        # The default height per height zone is 20 meters
        default_zone_height = 20

        # we take the ceiling of the quotient of the building height divided by the default zone height

        """
        +---------+     ----+
        |         | 6m      |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         +---> 5 height zones
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+         |
        |         |         |
        |         | 20m     |
        |         |         |
        +---------+     ----+
        """

        self.hz_num = math.ceil(dimensions.height / default_zone_height)

        self.height_zones = []
        height_sum = 0
        for i in range(1, self.hz_num + 1):
            # the last height zone may be less than the default zone height, in which case we simply take the height of
            # the building
            if i == self.hz_num:
                height_sum = dimensions.height
            else:
                height_sum += 20
            self.height_zones.append(HeightZone(zone_num=i, elevation=height_sum))


if __name__ == '__main__':
    dimensions = Dimensions(height=86, width=50)
    cladding = Cladding(2, 2)
    roof = Roof(50, 50, 45)
    building = Building(dimensions, cladding, roof, 0)
    print([str(x) for x in building.height_zones])

