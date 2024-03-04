from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import compute_wall_load_combinations


def process_wall_load_combination_data(building: Building, snow_load: SnowLoad, uls_wall_type: str, sls_wall_type: str):
    uls_wall_type = ULSWallLoadCombinationTypes(uls_wall_type)
    sls_wall_type = SLSWallLoadCombinationTypes(sls_wall_type)
    return compute_wall_load_combinations(building, snow_load, uls_wall_type, sls_wall_type)



