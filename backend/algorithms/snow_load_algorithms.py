import math

from backend.Constants.importance_factor_constants import WindImportanceFactor
from backend.Constants.snow_constants import RoofType
from backend.Constants.wind_constants import WindExposureFactorSelections
from backend.Entities.building import Building
from backend.Entities.snow import SnowLoad


def get_slope_factor(snow_load: SnowLoad, selection: RoofType, building: Building):
    match selection:
        case selection.UNOBSTRUCTED_SLIPPERY_ROOF:
            if building.roof.slope <= 15:
                snow_load.factor.cs = 1
            elif 15 < building.roof.slope < 60:
                snow_load.factor.cs = (60 - building.roof.slope) / 45
            elif building.roof.slope > 60:
                snow_load.factor.cs = 0
        case selection.OTHER:
            if building.roof.slope <= 30:
                snow_load.factor.cs = 1
            elif 30 < building.roof.slope < 70:
                snow_load.factor.cs = (70 - building.roof.slope) / 40
            elif building.roof.slope > 70:
                snow_load.factor.cs = 0


def get_accumulation_factor(snow_load: SnowLoad):
    snow_load.factor.ca = 1


def get_wind_exposure_factor(snow_load: SnowLoad, importance_selection: WindImportanceFactor, wind_exposure_factor_selection: WindExposureFactorSelections):
    if importance_selection in {importance_selection.SLS_LOW,
                                importance_selection.ULS_LOW,
                                importance_selection.SLS_NORMAL,
                                importance_selection.ULS_NORMAL} and wind_exposure_factor_selection == wind_exposure_factor_selection.INTERMEDIATE:
        snow_load.factor.cw = 0.75
    elif importance_selection in {importance_selection.SLS_LOW,
                                importance_selection.ULS_LOW,
                                importance_selection.SLS_NORMAL,
                                importance_selection.ULS_NORMAL} and wind_exposure_factor_selection == wind_exposure_factor_selection.OPEN:
        snow_load.factor.cw = 0.5
    else:
        snow_load.factor.cw = 1


def get_basic_roof_now_load_factor(snow_load: SnowLoad, building: Building):
    lc = 2 * building.roof.w_roof - building.roof.w_roof ** 2 / building.roof.l_roof
    if lc <= (70 / snow_load.factor.cw ** 2):
        snow_load.factor.cb = 0.8
    else:
        snow_load.factor.cb = (1 / snow_load.factor.cw) * (1 - (1 - 0.8 * snow_load.factor.cw) * math.exp(-1 * ((lc * snow_load.factor.cw ** 2 - 70) / (100))))


def get_snow_load(snow_load: SnowLoad, ls: float, ss: float, sr: float, manual=None):
    if manual is not None:
        snow_load.s = manual
    else:
        snow_load.s = ls * (ss * (snow_load.factor.cb * snow_load.factor.cw * snow_load.factor.cs * snow_load.factor.ca) + sr)




