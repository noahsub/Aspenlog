from enum import Enum


class ULSWallLoadCombinationTypes(Enum):
    ULS_DEAD_ONLY_1_4_D: str = 'uls_dead_only_1.4D'
    ULS_FULL_WIND_1_25D_1_4WY_0_5S: str = 'uls_full_wind_1.25D_1.4Wy_0.5S'
    ULS_FULL_SNOW_1_25D_1_5S_0_4WY: str = 'uls_full_snow_1.25D_1.5S_0.4Wy'
    ULS_SEISMIC_1_0D_1_0EY_0_25S: str = 'uls_seismic_1.0D_1.0Ey_0.25S'
    ULS_SEISMIC_1_0D_1_0EX_0_25S: str = 'uls_seismic_1.0D_1.0Ex_0.25S'


class SLSWallLoadCombinationTypes(Enum):
    SLS_1_0D_1_0WY: str = 'sls_1.0D_1.0Wy'
