from backend.Constants.wind_constants import WindExposureFactorSelections
from backend.Entities.building import Building


def get_wind_topographic_factor(ct: float = 1):
    return ct


def get_wind_exposure_factor(selection: WindExposureFactorSelections, building: Building):
    ce = None
    cei = None

    match selection:
        case selection.OPEN:
            ce = max((building.dimensions.height / 10) ** 0.2, 0.9)

            if building.h_opening != 0 and building.dimensions.height > 20:
                cei = (building.h_opening / 10) ** 0.2
            else:
                cei = max((building.dimensions.height / 20) ** 0.2, 0.6 ** 0.2)

        case selection.ROUGH:
            ce = max(0.7 * (building.dimensions.height / 12) ** 0.3, 0.7)

            if building.h_opening != 0 and building.dimensions.height > 20:
                cei = (building.h_opening / 12) ** 0.2
            else:
                cei = max((building.dimensions.height / 24) ** 0.3, 0.5 ** 0.3)

        case selection.INTERMEDIATE:
            # TODO: What do I do in this case?
            pass

    return ce, cei


