from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Constants.snow_constants import WindDirection, RoofType
from backend.Constants.wind_constants import WindExposureFactorSelections
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Snow.snow_factor import SnowFactorBuilder
from backend.Entities.Snow.snow_load import SnowLoadBuilder
from backend.algorithms.snow_load_algorithms import get_slope_factor, get_accumulation_factor, \
    get_wind_exposure_factor_snow, get_basic_roof_snow_load_factor, get_snow_load


def process_snow_load_data(building: Building, location: Location, importance_category: ImportanceFactor, exposure_factor_selection: str, roof_type: str):
    exposure_factor_selection = WindExposureFactorSelections(exposure_factor_selection)
    roof_type = RoofType(roof_type)

    snow_factor_builder_downwind = SnowFactorBuilder()
    snow_factor_builder_upwind = SnowFactorBuilder()

    # downwind snow_load
    get_slope_factor(snow_factor_builder_downwind, roof_type, building)
    get_accumulation_factor(snow_factor_builder_downwind, WindDirection.DOWNWIND, building)
    get_wind_exposure_factor_snow(snow_factor_builder_downwind, importance_category, exposure_factor_selection)
    get_basic_roof_snow_load_factor(snow_factor_builder_downwind, building)
    snow_load_builder_downwind = SnowLoadBuilder()
    get_snow_load(snow_factor_builder_downwind, snow_load_builder_downwind, importance_category, location)

    # upwind snow_load
    get_slope_factor(snow_factor_builder_upwind, roof_type, building)
    get_accumulation_factor(snow_factor_builder_upwind, WindDirection.UPWIND, building)
    get_wind_exposure_factor_snow(snow_factor_builder_upwind, importance_category, exposure_factor_selection)
    get_basic_roof_snow_load_factor(snow_factor_builder_upwind, building)
    snow_load_builder_upwind = SnowLoadBuilder()
    get_snow_load(snow_factor_builder_upwind, snow_load_builder_upwind, importance_category, location)

    snow_load_downwind = snow_load_builder_downwind.get_snow_load()
    snow_load_upwind = snow_load_builder_upwind.get_snow_load()

    return {
        "downwind": snow_load_downwind,
        "upwind": snow_load_upwind
    }
