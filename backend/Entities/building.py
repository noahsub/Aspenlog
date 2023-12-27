import math
from typing import Optional, Dict

from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.materials import Materials


class Dimensions:
    height: Optional[float]
    height_eave: Optional[float]
    height_ridge: Optional[float]
    width: float

    def __init__(self, width: float, height: float = None, height_eave: float = None, height_ridge: float = None):
        self.width = width
        if height_eave is not None and height_ridge is not None:
            self.height_eave = height_eave
            self.height_ridge = height_ridge
            self.height = (height_eave + height_ridge) / 2
        else:
            self.height = height


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
    wp: float

    def __init__(self, w_roof: float, l_roof: float, slope: float, wp: float):
        self.w_roof = w_roof
        self.l_roof = l_roof
        self.slope = slope
        if 30 <= slope <= 70:
            self.wall_slope = 1
        else:
            self.wall_slope = 0
        self.wp = wp


class HeightZone:
    zone_num: int
    elevation: float
    wp_materials: Optional[Dict[Materials, float]]

    def __init__(self, zone_num: int, elevation: float):
        self.zone_num = zone_num
        self.elevation = elevation
        self.wp_materials = None

    def __str__(self):
        return f"hz{self.zone_num}: {self.elevation}m"


class Building:
    dimensions: Dimensions
    cladding: Cladding
    roof: Roof
    hz_num: Optional[int]
    num_floor: int
    h_opening: float
    height_zones: Optional[list[HeightZone]]
    wp: Optional[float]

    def __init__(self, dimensions: Dimensions, cladding: Cladding, roof: Roof, num_floor: int, h_opening: float):
        self.dimensions = dimensions
        self.cladding = cladding
        self.roof = roof
        self.num_floor = num_floor
        self.h_opening = h_opening
        self.hz_num = None
        self.height_zones = None
        self.wp = None

    def compute_height_zones(self, selection: DefaultSelections, height_zones: list[HeightZone] = None):
        match selection:
            case selection.DEFAULT:
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
                    # the last height zone may be less than the default zone height, in which case we simply take the
                    # height of the building
                    if i == self.hz_num:
                        height_sum = dimensions.height
                    else:
                        height_sum += 20
                    self.height_zones.append(HeightZone(zone_num=i, elevation=height_sum))
            case selection.CUSTOM:
                self.height_zones = height_zones

    def compute_dead_load(self, selection: DefaultSelections, wp: float):
        match selection:
            case selection.DEFAULT:
                self.wp = wp
            case selection.CUSTOM:
                # ensure that all height zones have a valid material mapping
                assert all([height_zone.wp_materials is not None and
                            len(height_zone.wp_materials) <= len(Materials.get_materials_list())
                            for height_zone in self.height_zones])
                # compute dead load as weighted average based on material percentages and elevation
                self.wp = 0
                products = []
                material_sum = 0
                for height_zone in self.height_zones:
                    product = sum(x * height_zone.elevation for x in height_zone.wp_materials.values())
                    products.append(product)
                    material_sum += sum(height_zone.wp_materials.values())
                self.wp = sum(products) / material_sum


if __name__ == '__main__':
    dimensions = Dimensions(height=86, width=50)
    cladding = Cladding(2, 2)
    roof = Roof(50, 50, 45)
    building = Building(dimensions, cladding, roof, 0)
    print([str(x) for x in building.height_zones])
