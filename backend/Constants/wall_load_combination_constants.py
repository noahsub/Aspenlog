from enum import Enum


class ULSWallLoadCombinationTypes(Enum):
    ULS_DEAD_ONLY_1_4_D: str = 'uls_dead_only_1.4D'
    ULS_FULL_WIND_1_25D_1_4WY: str = 'uls_full_wind_1.25D_1.4Wy'
    ULS_SEISMIC_1_0D_1_0EY: str = 'uls_seismic_1.0D_1.0Ey'
    ULS_SEISMIC_1_0D_1_0EX: str = 'uls_seismic_1.0D_1.0Ex'


class SLSWallLoadCombinationTypes(Enum):
    SLS_1_0D_1_0WY: str = 'sls_1.0D_1.0Wy'
