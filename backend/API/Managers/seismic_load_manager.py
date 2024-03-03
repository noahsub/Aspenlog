from copy import deepcopy

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Seismic.seismic_factor import SeismicFactorBuilder
from backend.Entities.Seismic.seismic_load import SeismicLoadBuilder
from backend.algorithms.seismic_load_algorithms import get_seismic_factor_values, get_height_factor, \
    get_horizontal_force_factor, get_specified_lateral_earthquake_force


def process_seismic_load_data(building: Building, location: Location, importance_category: ImportanceFactor, ar: float, rp: float, cp: float):
    seismic_factor_builder = SeismicFactorBuilder()
    get_seismic_factor_values(seismic_factor_builder, ar, rp, cp)
    for height_zone in building.height_zones:
        zone_seismic_factor_builder = deepcopy(seismic_factor_builder)
        seismic_load_builder = SeismicLoadBuilder()
        get_height_factor(seismic_load_builder, building, height_zone.zone_num)
        get_horizontal_force_factor(zone_seismic_factor_builder, seismic_load_builder)
        get_specified_lateral_earthquake_force(seismic_load_builder, building, height_zone.zone_num, location, importance_category)
        seismic_load = seismic_load_builder.get_seismic_load()
        height_zone.seismic_load = seismic_load
