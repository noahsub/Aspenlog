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

from backend.Constants.importance_factor_constants import WindImportanceFactor, ImportanceFactor, LimitState
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections, \
    INTERNAL_GUST_EFFECT_FACTOR
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Wind.wind_factor import WindFactorBuilder, WindFactor
from backend.Entities.Wind.wind_load import WindLoad, WindLoadBuilder
from backend.Entities.Wind.wind_pressure import WindPressureBuilder


########################################################################################################################
# WIND LOAD ALGORITHMS
########################################################################################################################

def get_wind_topographic_factor(wind_factor_builder: WindFactorBuilder, ct: float = 1):
    """
    This function sets the topographic factor
    :param wind_load: A WindLoad object, responsible for storing the wind load information
    :param ct: Topographic factor
    :return: None
    """
    # Set the topographic factor of the wind load object
    wind_factor_builder.set_ct(ct)


def get_wind_exposure_factor(wind_factor_builder: WindFactorBuilder, selection: WindExposureFactorSelections,
                             building: Building, zone_num: int, manual: float = None):
    """
    This function sets the exposure factor
    :param wind_load:
    :param selection:
    :param building:
    :param manual:
    :return: None
    """

    height_zone = building.get_zone(zone_num)[0]

    # Different cases based on the wind exposure factor
    match selection:
        # If wind exposure factor is open
        case selection.OPEN:
            # ce = max((H / 10) ** 0.2, 0.9)
            wind_factor_builder.set_ce(max((height_zone.elevation / 10) ** 0.2, 0.9))
            # If dominant opening is not 0 and the height of the building is greater than 20m, set
            # cei = (H_opening/10)**0.2
            if building.h_opening != 0 and height_zone.elevation > 20:
                wind_factor_builder.set_cei((building.h_opening / 10) ** 0.2)
            # Otherwise set cei = max ((H / 20)**0.2, (0.6)**0.2
            else:
                wind_factor_builder.set_cei(max((height_zone.elevation / 20) ** 0.2, 0.6 ** 0.2))
        # If wind exposure factor is rough
        case selection.ROUGH:
            # ce = max((H / 12) ** 0.3, 0.7)
            wind_factor_builder.set_ce(max(0.7 * (height_zone.elevation / 12) ** 0.3, 0.7))
            # If dominant opening is not 0 and the height of the building is greater than 20m, set
            # cei = (H_opening / 12)**0.2
            if building.h_opening != 0 and height_zone.elevation > 20:
                wind_factor_builder.set_cei((building.h_opening / 12) ** 0.2)
            # Otherwise set cei = max ((H / 24)**0.3, (0.5)**0.3
            else:
                wind_factor_builder.set_cei(max((height_zone.elevation / 24) ** 0.3, 0.5 ** 0.3))
        # If wind exposure factor is intermediate, manually set ce and cei values
        # Note that ce == cei in this case
        case selection.INTERMEDIATE:
            wind_factor_builder.set_ce(manual)
            wind_factor_builder.set_cei(manual)


def get_wind_gust_factor(wind_factor_builder: WindFactorBuilder):
    wind_factor_builder.set_cg()


def get_internal_pressure(wind_factor: WindFactor, wind_pressure_builder: WindPressureBuilder, selection: InternalPressureSelections, importance_factor: ImportanceFactor, limit_state: LimitState, location: Location):
    """
    This function sets the internal pressure
    :param wind_load: A WindLoad object, responsible for storing the wind load information
    :param selection: The internal pressure to use in the computation
    :param wind_importance_factor: The wind importance factor to use in the computation
    :param location: A Location object, responsible for storing the location information
    :return:
    """

    wind_importance_factor = None
    match importance_factor:
        case importance_factor.LOW:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_LOW
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_LOW
        case importance_factor.NORMAL:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_NORMAL
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_NORMAL
        case importance_factor.HIGH:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_HIGH
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_HIGH
        case importance_factor.POST_DISASTER:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_POST_DISASTER
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_POST_DISASTER

    # A = (Iw * q * Cei * Ct * Cgi) * X where, x is the cpi_pos or cpi_neg value
    internal_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_factor.cei * wind_factor.ct * INTERNAL_GUST_EFFECT_FACTOR)

    # Different cases based on the internal pressure selection
    match selection:
        # If internal pressure is enclosed, set pi_pos = A * 0 and pi_neg = A * -0.15
        case selection.ENCLOSED:
            wind_pressure_builder.set_pi_pos(internal_pressure * 0)
            wind_pressure_builder.set_pi_neg(internal_pressure * -0.15)
        # If internal pressure is partially enclosed, set pi_pos = A * 0.3 and pi_neg = A * -0.45
        case selection.PARTIALLY_ENCLOSED:
            wind_pressure_builder.set_pi_pos(internal_pressure * 0.3)
            wind_pressure_builder.set_pi_neg(internal_pressure * -0.45)
        # If internal pressure is open, set pi_pos = A * 0.7 and pi_neg = A * -0.7
        case selection.LARGE_OPENINGS:
            wind_pressure_builder.set_pi_pos(internal_pressure * 0.7)
            wind_pressure_builder.set_pi_neg(internal_pressure * -0.7)


def get_external_pressure(wind_factor: WindFactor, wind_pressure_builder: WindPressureBuilder, importance_factor: ImportanceFactor, limit_state: LimitState, location: Location):
    wind_importance_factor = None
    match importance_factor:
        case importance_factor.LOW:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_LOW
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_LOW
        case importance_factor.NORMAL:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_NORMAL
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_NORMAL
        case importance_factor.HIGH:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_HIGH
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_HIGH
        case importance_factor.POST_DISASTER:
            match limit_state:
                case limit_state.ULS:
                    wind_importance_factor = WindImportanceFactor.ULS_POST_DISASTER
                case limit_state.SLS:
                    wind_importance_factor = WindImportanceFactor.SLS_POST_DISASTER

    # A = (Iw * q * Ce * Ct * Cg) * X where, x is the cpi_pos or cpi_neg value
    external_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_factor.ce * wind_factor.ct * wind_factor.cg)

    # Apply calculation to each zone
    for zone in wind_load.zones:
        # Different cases based on the zone type
        match zone.name:
            # If zone is roof interior, set pe_pos = A * 0 and pe_neg = A * -1
            case 'roof_interior':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -1
            # If zone is roof edge, set pe_pos = A * 0 and pe_neg = A * -1.5
            case 'roof_edge':
                wind_load.get_zone('roof_edge').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_edge').pressure.pe_neg = external_pressure * -1.5
            # If zone is roof corner, set pe_pos = A * 0 and pe_neg = A * -2.3
            case 'roof_corner':
                wind_load.get_zone('roof_corner').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_corner').pressure.pe_neg = external_pressure * -2.3
            # If zone is wall centre, set pe_pos = A * 0.9 and pe_neg = A * -0.9
            case 'wall_centre':
                wind_load.get_zone('wall_centre').pressure.pe_pos = external_pressure * 0.9
                wind_load.get_zone('wall_centre').pressure.pe_neg = external_pressure * -0.9
            # If zone is wall corner, set pe_pos = A * 0.9 and pe_neg = A * -1.2
            case 'wall_corner':
                wind_load.get_zone('wall_corner').pressure.pe_pos = external_pressure * 0.9
                wind_load.get_zone('wall_corner').pressure.pe_neg = external_pressure * -1.2

        # The pi_pos and pi_neg values are the same across all zones
        zone.pressure.pi_pos = wind_load.pressure.pi_pos
        zone.pressure.pi_neg = wind_load.pressure.pi_neg
