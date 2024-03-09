import itertools
from enum import Enum


class ULSWallLoadCombinationTypes(Enum):
    ULS_1_4_D: str = 'uls_1.4D'
    ULS_1_25D_1_4WY: str = 'uls_1.25D_1.4Wy'
    ULS_0_9D_1_4WX: str = 'uls_0.9D_1.4Wx'
    ULS_1_0D_1_0EY: str = 'uls_1.0D_1.0Ey'
    ULS_1_0D_1_0EX: str = 'uls_1.0D_1.0Ex'


class SLSWallLoadCombinationTypes(Enum):
    SLS_1_0D_1_0WY: str = 'sls_1.0D_1.0Wy'
    SLS_1_0D_1_0WX: str = 'sls_1.0D_1.0Wx'
