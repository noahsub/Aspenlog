from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import compute_wall_load_combinations


def process_wall_load_combination_data(building: Building, snow_load_downwind: SnowLoad, uls_wall_type: str, sls_wall_type: str):
    combinations = []
    for zone in building.height_zones:
        zone_num = zone.zone_num
        zone_combination = compute_wall_load_combinations(building, zone_num, snow_load_downwind, uls_wall_type, sls_wall_type)
        combinations.append(zone_combination)


