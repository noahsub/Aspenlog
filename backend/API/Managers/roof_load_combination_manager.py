from backend.Constants.roof_load_combination_constants import SLSRoofLoadCombinationTypes, ULSRoofLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import compute_roof_load_combinations


def process_roof_load_combination_data(building: Building, snow_load_upwind: SnowLoad, snow_load_downwind: SnowLoad,
                                       uls_roof_type: str, sls_roof_type: str):
    uls_wall_type = ULSRoofLoadCombinationTypes(uls_roof_type)
    sls_wall_type = SLSRoofLoadCombinationTypes(sls_roof_type)
    upwind_roof_combination = compute_roof_load_combinations(building, snow_load_upwind, uls_wall_type, sls_wall_type)
    downwind_roof_combination = compute_roof_load_combinations(building, snow_load_downwind, uls_wall_type,
                                                               sls_wall_type)
    return {'upwind': upwind_roof_combination, 'downwind': downwind_roof_combination}
