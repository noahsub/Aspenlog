from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.Building.building import Building
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Location.location import Location
from backend.Entities.Wind.wind_factor import WindFactorBuilder
from backend.Entities.Wind.wind_load import WindLoadBuilder
from backend.Entities.Wind.wind_pressure import WindPressureBuilder
from backend.algorithms.wind_load_algorithms import get_wind_topographic_factor, get_wind_exposure_factor, \
    get_wind_gust_factor, get_external_pressure, get_internal_pressure


def process_wind_load_data(building: Building, height_zone: HeightZone, importance_category: ImportanceFactor, location: Location, ct: float, exposure_factor: str, internal_pressure_category: str, manual_ce_cei: float=None):
    wind_factor_builder = WindFactorBuilder()
    get_wind_topographic_factor(wind_factor_builder, ct)
    exposure_factor_selection = WindExposureFactorSelections(exposure_factor)
    if exposure_factor_selection == WindExposureFactorSelections.INTERMEDIATE:
        get_wind_exposure_factor(wind_factor_builder, exposure_factor_selection, building, height_zone.zone_num, manual_ce_cei)
    else:
        get_wind_exposure_factor(wind_factor_builder, exposure_factor_selection, building, height_zone.zone_num)
    get_wind_gust_factor(wind_factor_builder)
    wind_factor = wind_factor_builder.get_wind_factor()
    wind_pressure_builder = WindPressureBuilder()
    internal_pressure_selection = InternalPressureSelections(internal_pressure_category)
    get_internal_pressure(wind_factor, wind_pressure_builder, internal_pressure_selection, importance_category, location)
    wind_load_builder = WindLoadBuilder()
    get_external_pressure(wind_factor, wind_pressure_builder, wind_load_builder, importance_category, location)
    wind_load = wind_load_builder.get_wind_load()
    height_zone.wind_load = wind_load
