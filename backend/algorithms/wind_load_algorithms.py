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

from backend.Constants.importance_factor_constants import WindImportanceFactor
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.building import Building
from backend.Entities.location import Location
from backend.Entities.wind import WindLoad


########################################################################################################################
# WIND LOAD ALGORITHMS
########################################################################################################################

def get_wind_topographic_factor(wind_load: WindLoad, ct: float = 1):
    """
    This function sets the topographic factor
    :param wind_load: A WindLoad object, responsible for storing the wind load information
    :param ct: Topographic factor
    :return: None
    """
    # Set the topographic factor of the wind load object
    wind_load.factor.ct = ct


def get_wind_exposure_factor(wind_load: WindLoad, selection: WindExposureFactorSelections, building: Building, manual: float = None):
    """
    This function sets the exposure factor
    :param wind_load:
    :param selection:
    :param building:
    :param manual:
    :return: None
    """
    # Different cases based on the wind exposure factor
    match selection:
        # If wind exposure factor is open
        case selection.OPEN:
            # ce = max((H / 10) ** 0.2, 0.9)
            wind_load.factor.ce = max((building.dimensions.height / 10) ** 0.2, 0.9)
            # If dominant opening is not 0 and the height of the building is greater than 20m, set
            # cei = (H_opening/10)**0.2
            if building.h_opening != 0 and building.dimensions.height > 20:
                wind_load.factor.cei = (building.h_opening / 10) ** 0.2
            # Otherwise set cei = max ((H / 20)**0.2, (0.6)**0.2
            else:
                wind_load.factor.cei = max((building.dimensions.height / 20) ** 0.2, 0.6 ** 0.2)
        # If wind exposure factor is rough
        case selection.ROUGH:
            # ce = max((H / 12) ** 0.3, 0.7)
            wind_load.factor.ce = max(0.7 * (building.dimensions.height / 12) ** 0.3, 0.7)
            # If dominant opening is not 0 and the height of the building is greater than 20m, set
            # cei = (H_opening / 12)**0.2
            if building.h_opening != 0 and building.dimensions.height > 20:
                wind_load.factor.cei = (building.h_opening / 12) ** 0.2
            # Otherwise set cei = max ((H / 24)**0.3, (0.5)**0.3
            else:
                wind_load.factor.cei = max((building.dimensions.height / 24) ** 0.3, 0.5 ** 0.3)
        # If wind exposure factor is intermediate, manually set ce and cei values
        # Note that ce == cei in this case
        case selection.INTERMEDIATE:
            wind_load.factor.ce = manual
            wind_load.factor.cei = manual


def get_internal_pressure(wind_load: WindLoad, selection: InternalPressureSelections, wind_importance_factor: WindImportanceFactor, location: Location):
    """
    This function sets the internal pressure
    :param wind_load: A WindLoad object, responsible for storing the wind load information
    :param selection: The internal pressure to use in the computation
    :param wind_importance_factor: The wind importance factor to use in the computation
    :param location: A Location object, responsible for storing the location information
    :return:
    """
    # A = (Iw * q * Cei * Ct * Cgi) * X where, x is the cpi_pos or cpi_neg value
    internal_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_load.factor.cei * wind_load.factor.ct * 2)

    # Different cases based on the internal pressure selection
    match selection:
        # If internal pressure is enclosed, set pi_pos = A * 0 and pi_neg = A * -0.15
        case selection.ENCLOSED:
            wind_load.pressure.pi_pos = internal_pressure * 0
            wind_load.pressure.pi_neg = internal_pressure * -0.15
        # If internal pressure is partially enclosed, set pi_pos = A * 0.3 and pi_neg = A * -0.45
        case selection.PARTIALLY_ENCLOSED:
            wind_load.pressure.pi_pos = internal_pressure * 0.3
            wind_load.pressure.pi_neg = internal_pressure * -0.45
        # If internal pressure is open, set pi_pos = A * 0.7 and pi_neg = A * -0.7
        case selection.LARGE_OPENINGS:
            wind_load.pressure.pi_pos = internal_pressure * 0.7
            wind_load.pressure.pi_neg = internal_pressure * -0.7


def get_external_pressure(wind_load: WindLoad, wind_importance_factor: WindImportanceFactor, location: Location):
    # A = (Iw * q * Ce * Ct * Cg) * X where, x is the cpi_pos or cpi_neg value
    external_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_load.factor.ce * wind_load.factor.ct * wind_load.factor.cg)

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
