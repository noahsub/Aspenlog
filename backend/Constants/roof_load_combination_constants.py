from enum import Enum


class ULSRoofLoadCombinationTypes(Enum):
    ULS_DEAD_ONLY_1_4_D: str = 'dead_only_1.4D'
    ULS_FULL_WIND_1_25D_1_4WY: str = 'full_wind_1.25D_1.4Wy'
    ULS_SEISMIC_1_0D_1_0EY: str = 'seismic_1.0D_1.0Ey'
    ULS_SEISMIC_1_0D_1_0EX: str = 'seismic_1.0D_1.0Ex'
    ULS_FULL_SNOW_WITH_WIND_1_25D_1_5S: str = 'full_snow_with_wind_1.25D_1.5S'


class SLSRoofLoadCombinationTypes(Enum):
    SLS_DEAD_AND_WIND_Y_NORMAL_TO_FACE_1_0D_1_0WY: str = 'dead_and_wind_Y_normal_to_face_1.0D_1.0Wy'
    SLS_SNOW_WITH_WIND_1_0D_1_0S: str = 'snow_with_wind_1.0D_1.0S'
    SLS_DEAD_AND_LIVE_1_0D_1_0L: str = 'dead_and_live_1.0D_1.0L'
