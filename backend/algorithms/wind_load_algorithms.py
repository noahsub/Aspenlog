from backend.Constants.importance_factor_constants import WindImportanceFactor
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.building import Building
from backend.Entities.location import Location
from backend.Entities.wind import WindFactor, WindLoad


def get_wind_topographic_factor(wind_load: WindLoad, ct: float = 1):
    wind_load.factor.ct = ct


def get_wind_exposure_factor(wind_load: WindLoad, selection: WindExposureFactorSelections, building: Building, manual=None):
    match selection:
        case selection.OPEN:
            wind_load.factor.ce = max((building.dimensions.height / 10) ** 0.2, 0.9)

            if building.h_opening != 0 and building.dimensions.height > 20:
                wind_load.factor.cei = (building.h_opening / 10) ** 0.2
            else:
                wind_load.factor.cei = max((building.dimensions.height / 20) ** 0.2, 0.6 ** 0.2)

        case selection.ROUGH:
            wind_load.factor.ce = max(0.7 * (building.dimensions.height / 12) ** 0.3, 0.7)

            if building.h_opening != 0 and building.dimensions.height > 20:
                wind_load.factor.cei = (building.h_opening / 12) ** 0.2
            else:
                wind_load.factor.cei = max((building.dimensions.height / 24) ** 0.3, 0.5 ** 0.3)

        case selection.INTERMEDIATE:
            wind_load.factor.ce = manual
            wind_load.factor.cei = manual


def get_internal_pressure(wind_load: WindLoad, selection: InternalPressureSelections, wind_importance_factor: WindImportanceFactor, location: Location):
    internal_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_load.factor.cei * wind_load.factor.ct * 2)

    match selection:
        case selection.ENCLOSED:
            wind_load.pressure.pi_pos = internal_pressure * 0
            wind_load.pressure.pi_neg = internal_pressure * -0.15
        case selection.PARTIALLY_ENCLOSED:
            wind_load.pressure.pi_pos = internal_pressure * 0.3
            wind_load.pressure.pi_neg = internal_pressure * -0.45
        case selection.LARGE_OPENINGS:
            wind_load.pressure.pi_pos = internal_pressure * 0.7
            wind_load.pressure.pi_neg = internal_pressure * -0.7


def get_external_pressure(wind_load: WindLoad, wind_importance_factor: WindImportanceFactor, location: Location):
    external_pressure = (wind_importance_factor.value * location.wind_velocity_pressure * wind_load.factor.ce * wind_load.factor.ct * wind_load.factor.cg)

    for zone in wind_load.zones:
        match zone.name:
            case 'roof_interior':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -1
            case 'roof_edge':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -1.5
            case 'roof_corner':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -2.3
            case 'wall_centre':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0.9
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -0.9
            case 'wall_corner':
                wind_load.get_zone('roof_interior').pressure.pe_pos = external_pressure * 0.9
                wind_load.get_zone('roof_interior').pressure.pe_neg = external_pressure * -1.2

        zone.pressure.pi_pos = wind_load.pressure.pi_pos
        zone.pressure.pi_neg = wind_load.pressure.pi_neg
