########################################################################################################################
# snow_load_algorithms.py
# This file contains the algorithms for calculating snow load
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import math
from backend.Constants.importance_factor_constants import WindImportanceFactor, SnowImportanceFactor, ImportanceFactor, \
    LimitState
from backend.Constants.load_constants import LoadTypes
from backend.Constants.snow_constants import RoofType, ACCUMULATION_FACTOR
from backend.Constants.wind_constants import WindExposureFactorSelections
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Snow.snow_factor import SnowFactorBuilder
from backend.Entities.Snow.snow_load import SnowLoadBuilder


########################################################################################################################
# SNOW LOAD ALGORITHMS
########################################################################################################################

def get_slope_factor(snow_factor_builder: SnowFactorBuilder, selection: RoofType, building: Building):
    """
    This function sets the slope factor
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param selection: The roof type
    :param building: A Building object, responsible for storing the building information
    :return:
    """
    # Different cases based on the roof type
    match selection:
        # If Unobstructed Slippery Roof
        case selection.UNOBSTRUCTED_SLIPPERY_ROOF:
            # If the slope of the roof is less than or equal to 15 degrees, set the slope factor to 1
            if building.roof.slope <= 15:
                snow_factor_builder.set_cs(1)
            # If the slope of the roof is between 15 and 60 degrees, set the slope factor to (60 - slope) / 45
            elif 15 < building.roof.slope < 60:
                snow_factor_builder.set_cs((60 - building.roof.slope) / 45)
            # If the slope of the roof is greater than 60 degrees, set the slope factor to 0
            elif building.roof.slope > 60:
                snow_factor_builder.set_cs(0)
        # If not Unobstructed Slippery Roof
        case selection.OTHER:
            # If the slope of the roof is less than or equal to 30 degrees, set the slope factor to 1
            if building.roof.slope <= 30:
                snow_factor_builder.set_cs(1)
            # If the slope of the roof is between 30 and 70 degrees, set the slope factor to (70 - slope) / 40
            elif 30 < building.roof.slope < 70:
                snow_factor_builder.set_cs((70 - building.roof.slope) / 40)
            # If the slope of the roof is greater than 70 degrees, set the slope factor to 0
            elif building.roof.slope > 70:
                snow_factor_builder.set_cs(0)


def get_accumulation_factor(snow_factor_builder: SnowFactorBuilder):
    snow_factor_builder.set_ca(ACCUMULATION_FACTOR)


def get_wind_exposure_factor_snow(snow_factor_builder: SnowFactorBuilder, importance_factor: ImportanceFactor, wind_exposure_factor_selection: WindExposureFactorSelections):
    """
    This function sets the wind exposure factor
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param importance_selection: The importance factor to use in the computation
    :param wind_exposure_factor_selection: The wind exposure factor to use in the computation
    :return:
    """

    # A set of importance factors that are considered low or normal
    low_or_normal = {ImportanceFactor.LOW, ImportanceFactor.NORMAL}

    # If the importance factor is low or normal and the wind exposure factor is intermediate, set the wind exposure factor to 0.75
    if importance_factor in low_or_normal and wind_exposure_factor_selection == wind_exposure_factor_selection.INTERMEDIATE:
        snow_factor_builder.set_cw(0.75)
    # If the importance factor is low or normal and the wind exposure factor is sheltered, set the wind exposure factor to 0.5
    elif importance_factor in low_or_normal and wind_exposure_factor_selection == wind_exposure_factor_selection.OPEN:
        snow_factor_builder.set_cw(0.5)
    # Otherwise, set the wind exposure factor to 1
    else:
        snow_factor_builder.set_cw(1)


def get_basic_roof_snow_load_factor(snow_factor_builder: SnowFactorBuilder, building: Building):
    """
    This function sets the basic roof snow load factor
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param building: A Building object, responsible for storing the building information
    :return: None
    """
    # Ic = 2 * w_roof - w_roof**2 / l_roof
    ic = 2 * building.roof.w_roof - building.roof.w_roof ** 2 / building.roof.l_roof
    # If ic is less than or equal to 70 divided by the wind exposure factor squared, set the basic roof snow load factor to 0.8
    if ic <= (70 / snow_factor_builder.get_cw() ** 2):
        snow_factor_builder.set_cb(0.8)
    # Otherwise, set the basic roof snow load factor to Cb = 1 / Cw * (1 - (1 - 0.8 * Cw)*exp*(-1 * (Ic * Cw**2 - 70) / 100))
    else:
        snow_factor_builder.set_cb((1 / snow_factor_builder.get_cw()) * (1 - (1 - 0.8 * snow_factor_builder.get_cw()) * math.exp(-1 * ((ic * snow_factor_builder.get_cw() ** 2 - 70) / (100)))))


def get_snow_load(snow_factor_builder: SnowFactorBuilder, snow_load_builder: SnowLoadBuilder, importance_factor: ImportanceFactor, location: Location):
    """
    This function sets the snow load
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param snow_importance_factor: The snow importance factor to use in the computation
    :param location: A Location object, responsible for storing the location information
    :return: None
    """
    snow_importance_factor_uls = importance_factor.get_importance_factor_uls(LoadTypes.SNOW)
    snow_importance_factor_sls = importance_factor.get_importance_factor_sls(LoadTypes.SNOW)

    snow_load_builder.set_s_uls(snow_importance_factor_uls * (location.rain_load * (snow_factor_builder.get_cb() * snow_factor_builder.get_cw() * snow_factor_builder.get_cs() * snow_factor_builder.get_ca()) + location.snow_load))
    snow_load_builder.set_s_sls(snow_importance_factor_sls * (location.rain_load * (snow_factor_builder.get_cb() * snow_factor_builder.get_cw() * snow_factor_builder.get_cs() * snow_factor_builder.get_ca()) + location.snow_load))
    snow_load_builder.set_factor(snow_factor_builder.get_snow_factor())
