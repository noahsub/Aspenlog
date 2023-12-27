from backend.Constants.importance_factor_constants import SeismicImportanceFactor
from backend.Entities.building import Building
from backend.Entities.location import Location
from backend.Entities.seismic import SeismicLoad
from backend.Entities.snow import SnowLoad


def get_seismic_factor_values(seismic_load: SeismicLoad, ar: float = 1, rp: float = 2.5, cp: float = 1):
    # if ar parameter is present
    if ar:
        seismic_load.factor.ar = ar
    # if rp parameter is present
    if rp:
        seismic_load.factor.rp = rp
    # if cp parameter is present
    if cp:
        seismic_load.factor.cp = cp


def get_floor_mapping(building: Building):
    # TODO: Needs to be optimized
    # TODO: Bug here. num_floor is a string when execution of this function is reached
    building.num_floor = int(int(building.num_floor))
    floor_height = building.dimensions.height / building.num_floor
    floor_mapping = {}
    for floor in range(1, building.num_floor + 1, 1):
        for zone in building.height_zones:
            if floor * floor_height <= zone.elevation:
                floor_mapping[floor] = zone.zone_num
                break
    return floor_mapping


def get_height_factor(seismic_load: SeismicLoad, building: Building, floor: int):
    seismic_load.ax = 1 + 2 * floor / building.dimensions.height

def get_horizontal_force_factor(seismic_load: SeismicLoad):
    seismic_load.sp = seismic_load.factor.cp * seismic_load.factor.ar * seismic_load.ax / seismic_load.factor.rp

def get_specified_laterial_earthquake_force(seismic_load: SeismicLoad, snow_load: SnowLoad, building: Building, location: Location, seismic_importance_factor: SeismicImportanceFactor):
    # Vp=0.3*S_0.2*Ie*Sp*Wp
    seismic_load.vp = 0.3 * location.design_spectral_acceleration_0_2 * seismic_importance_factor.value * seismic_load.sp * building.wp
    # Vp_snow=0.3*S_0.2*Ie*Wp_snow where Wp_snow=S+Wp
    seismic_load.vp_snow = 0.3 * location.design_spectral_acceleration_0_2 * seismic_importance_factor.value * (snow_load.s + building.wp)
