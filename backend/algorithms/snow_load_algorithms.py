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
from backend.Constants.importance_factor_constants import WindImportanceFactor, SnowImportanceFactor
from backend.Constants.snow_constants import RoofType
from backend.Constants.wind_constants import WindExposureFactorSelections
from backend.Entities.building import Building
from backend.Entities.location import Location
from backend.Entities.snow import SnowLoad


########################################################################################################################
# SNOW LOAD ALGORITHMS
########################################################################################################################

def get_slope_factor(snow_load: SnowLoad, selection: RoofType, building: Building):
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
                snow_load.factor.cs = 1
            # If the slope of the roof is between 15 and 60 degrees, set the slope factor to (60 - slope) / 45
            elif 15 < building.roof.slope < 60:
                snow_load.factor.cs = (60 - building.roof.slope) / 45
            # If the slope of the roof is greater than 60 degrees, set the slope factor to 0
            elif building.roof.slope > 60:
                snow_load.factor.cs = 0
        # If not Unobstructed Slippery Roof
        case selection.OTHER:
            # If the slope of the roof is less than or equal to 30 degrees, set the slope factor to 1
            if building.roof.slope <= 30:
                snow_load.factor.cs = 1
            # If the slope of the roof is between 30 and 70 degrees, set the slope factor to (70 - slope) / 40
            elif 30 < building.roof.slope < 70:
                snow_load.factor.cs = (70 - building.roof.slope) / 40
            # If the slope of the roof is greater than 70 degrees, set the slope factor to 0
            elif building.roof.slope > 70:
                snow_load.factor.cs = 0


# TODO: Depreciated, simply use constant when initializing SnowFactor object
# def get_accumulation_factor(snow_load: SnowLoad):
#     snow_load.factor.ca = 1


def get_wind_exposure_factor(snow_load: SnowLoad, importance_selection: WindImportanceFactor, wind_exposure_factor_selection: WindExposureFactorSelections):
    """
    This function sets the wind exposure factor
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param importance_selection: The importance factor to use in the computation
    :param wind_exposure_factor_selection: The wind exposure factor to use in the computation
    :return:
    """

    # A set of importance factors that are considered low or normal
    low_or_normal = {
        importance_selection.SLS_LOW,
        importance_selection.ULS_LOW,
        importance_selection.SLS_NORMAL,
        importance_selection.ULS_NORMAL
    }

    # If the importance factor is low or normal and the wind exposure factor is intermediate, set the wind exposure factor to 0.75
    if importance_selection in low_or_normal and wind_exposure_factor_selection == wind_exposure_factor_selection.INTERMEDIATE:
        snow_load.factor.cw = 0.75
    # If the importance factor is low or normal and the wind exposure factor is sheltered, set the wind exposure factor to 0.5
    elif importance_selection in low_or_normal and wind_exposure_factor_selection == wind_exposure_factor_selection.OPEN:
        snow_load.factor.cw = 0.5
    # Otherwise, set the wind exposure factor to 1
    else:
        snow_load.factor.cw = 1


def get_basic_roof_now_load_factor(snow_load: SnowLoad, building: Building):
    """
    This function sets the basic roof snow load factor
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param building: A Building object, responsible for storing the building information
    :return: None
    """
    # Ic = 2 * w_roof - w_roof**2 / l_roof
    ic = 2 * building.roof.w_roof - building.roof.w_roof ** 2 / building.roof.l_roof
    # If ic is less than or equal to 70 divided by the wind exposure factor squared, set the basic roof snow load factor to 0.8
    if ic <= (70 / snow_load.factor.cw ** 2):
        snow_load.factor.cb = 0.8
    # Otherwise, set the basic roof snow load factor to Cb = 1 / Cw * (1 - (1 - 0.8 * Cw)*exp*(-1 * (Ic * Cw**2 - 70) / 100))
    else:
        snow_load.factor.cb = (1 / snow_load.factor.cw) * (1 - (1 - 0.8 * snow_load.factor.cw) * math.exp(-1 * ((ic * snow_load.factor.cw ** 2 - 70) / (100))))


def get_snow_load(snow_load: SnowLoad, snow_importance_factor: SnowImportanceFactor, location: Location):
    """
    This function sets the snow load
    :param snow_load: A SnowLoad object, responsible for storing the snow load information
    :param snow_importance_factor: The snow importance factor to use in the computation
    :param location: A Location object, responsible for storing the location information
    :return: None
    """
    snow_load.s = snow_importance_factor.value * (location.rain_load * (snow_load.factor.cb * snow_load.factor.cw * snow_load.factor.cs * snow_load.factor.ca) + location.snow_load)
