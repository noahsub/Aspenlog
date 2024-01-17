########################################################################################################################
# snow_load_algorithms.py
# This file contains the algorithms for calculating snow load
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################
from copy import copy, deepcopy

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.importance_factor_constants import WindImportanceFactor, ImportanceFactor, LimitState
from backend.Constants.load_constants import LoadTypes
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections, \
    INTERNAL_GUST_EFFECT_FACTOR
from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.Wind.wind_factor import WindFactorBuilder, WindFactor
from backend.Entities.Wind.wind_load import WindLoad, WindLoadBuilder
from backend.Entities.Wind.wind_pressure import WindPressureBuilder
from backend.Entities.Wind.zone import ZoneBuilder


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


def get_wind_exposure_factor(wind_factor_builder: WindFactorBuilder, wind_exposure_factor_selection: WindExposureFactorSelections,
                             building: Building, zone_num: int, manual: float = None):
    """
    This function sets the exposure factor
    :param wind_load:
    :param wind_exposure_factor_selection:
    :param building:
    :param manual:
    :return: None
    """

    height_zone = building.get_zone(zone_num)[0]

    # Different cases based on the wind exposure factor
    match wind_exposure_factor_selection:
        # If wind exposure factor is open
        case wind_exposure_factor_selection.OPEN:
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
        case wind_exposure_factor_selection.ROUGH:
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
        case wind_exposure_factor_selection.INTERMEDIATE:
            wind_factor_builder.set_ce(manual)
            wind_factor_builder.set_cei(manual)


def get_wind_gust_factor(wind_factor_builder: WindFactorBuilder):
    wind_factor_builder.set_cg()


def get_internal_pressure(wind_factor: WindFactor, wind_pressure_builder: WindPressureBuilder, internal_pressure_selection: InternalPressureSelections, importance_factor: ImportanceFactor, location: Location):
    """
    This function sets the internal pressure
    :param wind_load: A WindLoad object, responsible for storing the wind load information
    :param internal_pressure_selection: The internal pressure to use in the computation
    :param wind_importance_factor: The wind importance factor to use in the computation
    :param location: A Location object, responsible for storing the location information
    :return:
    """

    wind_importance_factor_uls = importance_factor.get_importance_factor_uls(LoadTypes.WIND)
    wind_importance_factor_sls = importance_factor.get_importance_factor_sls(LoadTypes.WIND)


    # A = (Iw * q * Cei * Ct * Cgi) * X where, x is the cpi_pos or cpi_neg value
    internal_pressure_uls = (wind_importance_factor_uls * location.wind_velocity_pressure * wind_factor.cei * wind_factor.ct * INTERNAL_GUST_EFFECT_FACTOR)
    internal_pressure_sls = (wind_importance_factor_sls * location.wind_velocity_pressure * wind_factor.cei * wind_factor.ct * INTERNAL_GUST_EFFECT_FACTOR)

    # Different cases based on the internal pressure selection
    match internal_pressure_selection:
        # If internal pressure is enclosed, set pi_pos = A * 0 and pi_neg = A * -0.15
        case internal_pressure_selection.ENCLOSED:
            wind_pressure_builder.set_pi_pos_uls(internal_pressure_uls * 0)
            wind_pressure_builder.set_pi_neg_uls(internal_pressure_uls * -0.15)
            wind_pressure_builder.set_pi_pos_sls(internal_pressure_sls * 0)
            wind_pressure_builder.set_pi_neg_sls(internal_pressure_sls * -0.15)
        # If internal pressure is partially enclosed, set pi_pos = A * 0.3 and pi_neg = A * -0.45
        case internal_pressure_selection.PARTIALLY_ENCLOSED:
            wind_pressure_builder.set_pi_pos_uls(internal_pressure_uls * 0.3)
            wind_pressure_builder.set_pi_neg_uls(internal_pressure_uls * -0.45)
            wind_pressure_builder.set_pi_pos_sls(internal_pressure_sls * 0.3)
            wind_pressure_builder.set_pi_neg_sls(internal_pressure_sls * -0.45)
        # If internal pressure is open, set pi_pos = A * 0.7 and pi_neg = A * -0.7
        case internal_pressure_selection.LARGE_OPENINGS:
            wind_pressure_builder.set_pi_pos_uls(internal_pressure_uls * 0.7)
            wind_pressure_builder.set_pi_neg_uls(internal_pressure_uls * -0.7)
            wind_pressure_builder.set_pi_pos_sls(internal_pressure_sls * 0.7)
            wind_pressure_builder.set_pi_neg_sls(internal_pressure_sls * -0.7)


def get_external_pressure(wind_factor: WindFactor, wind_pressure_builder: WindPressureBuilder, wind_load_builder: WindLoadBuilder, importance_factor: ImportanceFactor, location: Location):
    wind_importance_factor_uls = importance_factor.get_importance_factor_uls(LoadTypes.WIND)
    wind_importance_factor_sls = importance_factor.get_importance_factor_sls(LoadTypes.WIND)

    # A = (Iw * q * Ce * Ct * Cg) * X where, x is the cpi_pos or cpi_neg value
    external_pressure_uls = (wind_importance_factor_uls * location.wind_velocity_pressure * wind_factor.ce * wind_factor.ct * wind_factor.cg)
    external_pressure_sls = (wind_importance_factor_sls * location.wind_velocity_pressure * wind_factor.ce * wind_factor.ct * wind_factor.cg)

    zone_types = [(1, 'roof_interior'), (2, 'roof_edge'), (3, 'roof_corner'), (4, 'wall_centre'), (5, 'wall_corner')]
    zones = []

    # Apply calculation to each zone
    for zone_type in zone_types:
        zone_wind_pressure_builder = deepcopy(wind_pressure_builder)
        zone_builder = ZoneBuilder()
        zone_builder.set_name(zone_type[1])
        zone_builder.set_num(zone_type[0])
        # Different cases based on the zone type
        match zone_type[1]:
            # If zone is roof interior, set pe_pos = A * 0 and pe_neg = A * -1
            case 'roof_interior':
                zone_wind_pressure_builder.set_pe_pos_uls(external_pressure_uls * 0)
                zone_wind_pressure_builder.set_pe_neg_uls(external_pressure_uls * -1)
                zone_wind_pressure_builder.set_pe_pos_sls(external_pressure_sls * 0)
                zone_wind_pressure_builder.set_pe_neg_sls(external_pressure_sls * -1)
            # If zone is roof edge, set pe_pos = A * 0 and pe_neg = A * -1.5
            case 'roof_edge':
                zone_wind_pressure_builder.set_pe_pos_uls(external_pressure_uls * 0)
                zone_wind_pressure_builder.set_pe_neg_uls(external_pressure_uls * -1.5)
                zone_wind_pressure_builder.set_pe_pos_sls(external_pressure_sls * 0)
                zone_wind_pressure_builder.set_pe_neg_sls(external_pressure_sls * -1.5)
            # If zone is roof corner, set pe_pos = A * 0 and pe_neg = A * -2.3
            case 'roof_corner':
                zone_wind_pressure_builder.set_pe_pos_uls(external_pressure_uls * 0)
                zone_wind_pressure_builder.set_pe_neg_uls(external_pressure_uls * -2.3)
                zone_wind_pressure_builder.set_pe_pos_sls(external_pressure_sls * 0)
                zone_wind_pressure_builder.set_pe_neg_sls(external_pressure_sls * -2.3)
            # If zone is wall centre, set pe_pos = A * 0.9 and pe_neg = A * -0.9
            case 'wall_centre':
                zone_wind_pressure_builder.set_pe_pos_uls(external_pressure_uls * 0.9)
                zone_wind_pressure_builder.set_pe_neg_uls(external_pressure_uls * -0.9)
                zone_wind_pressure_builder.set_pe_pos_sls(external_pressure_sls * 0.9)
                zone_wind_pressure_builder.set_pe_neg_sls(external_pressure_sls * -0.9)
            # If zone is wall corner, set pe_pos = A * 0.9 and pe_neg = A * -1.2
            case 'wall_corner':
                zone_wind_pressure_builder.set_pe_pos_uls(external_pressure_uls * 0.9)
                zone_wind_pressure_builder.set_pe_neg_uls(external_pressure_uls * -1.2)
                zone_wind_pressure_builder.set_pe_pos_sls(external_pressure_sls * 0.9)
                zone_wind_pressure_builder.set_pe_neg_sls(external_pressure_sls * -1.2)

        zone_wind_pressure_builder.set_pos_uls()
        zone_wind_pressure_builder.set_neg_uls()
        zone_wind_pressure_builder.set_pos_sls()
        zone_wind_pressure_builder.set_neg_sls()
        pressure = zone_wind_pressure_builder.get_wind_pressure()
        zone_builder.set_pressure(pressure)

        zones.append(zone_builder.get_zone())

    wind_load_builder.set_zones(zones)
    wind_load_builder.set_factor(wind_factor)
