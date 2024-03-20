########################################################################################################################
# wind_load_manager.py
# This file manages the wind load data for a building.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Constants.wind_constants import (
    WindExposureFactorSelections,
    InternalPressureSelections,
)
from backend.Entities.Building.building import Building
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Location.location import Location
from backend.Entities.Wind.wind_factor import WindFactorBuilder
from backend.Entities.Wind.wind_load import WindLoadBuilder
from backend.Entities.Wind.wind_pressure import WindPressureBuilder
from backend.algorithms.wind_load_algorithms import (
    get_wind_topographic_factor,
    get_wind_exposure_factor,
    get_wind_gust_factor,
    get_external_pressure,
    get_internal_pressure,
)

########################################################################################################################
# MANAGER
########################################################################################################################


def process_wind_load_data(
    building: Building,
    height_zone: HeightZone,
    importance_category: ImportanceFactor,
    location: Location,
    ct: float,
    exposure_factor: str,
    internal_pressure_category: str,
    manual_ce_cei: float = None,
):
    """
    Processes the wind load data for a building
    :param building: The building object
    :param height_zone: The height zone object
    :param importance_category: The importance category of the building
    :param location: The location of the building
    :param ct: The topographic factor
    :param exposure_factor: The exposure factor
    :param internal_pressure_category: The internal pressure category
    :param manual_ce_cei: The manual exposure factor for intermediate exposure
    :return: None
    """
    # Create a wind factor builder object
    wind_factor_builder = WindFactorBuilder()
    # Get the topographic factor
    get_wind_topographic_factor(wind_factor_builder, ct)
    # Get the exposure factor
    exposure_factor_selection = WindExposureFactorSelections(exposure_factor)
    # If the exposure factor is intermediate, get the exposure factor with the manual value
    if exposure_factor_selection == WindExposureFactorSelections.INTERMEDIATE:
        get_wind_exposure_factor(
            wind_factor_builder,
            exposure_factor_selection,
            building,
            height_zone.zone_num,
            manual_ce_cei,
        )
    # Otherwise, get the exposure factor without the manual value
    else:
        get_wind_exposure_factor(
            wind_factor_builder,
            exposure_factor_selection,
            building,
            height_zone.zone_num,
        )
    # Get the gust factor
    get_wind_gust_factor(wind_factor_builder)
    # Get the wind factor
    wind_factor = wind_factor_builder.get_wind_factor()
    # Create a wind pressure builder object
    wind_pressure_builder = WindPressureBuilder()
    # Get the internal pressure
    internal_pressure_selection = InternalPressureSelections(internal_pressure_category)
    # Get the internal pressure
    get_internal_pressure(
        wind_factor,
        wind_pressure_builder,
        internal_pressure_selection,
        importance_category,
        location,
    )
    # Create a wind load builder object
    wind_load_builder = WindLoadBuilder()
    # Get the external pressure
    get_external_pressure(
        wind_factor,
        wind_pressure_builder,
        wind_load_builder,
        importance_category,
        location,
    )
    # Get the wind load
    wind_load = wind_load_builder.get_wind_load()
    # Set the wind load for the height zone
    height_zone.wind_load = wind_load
