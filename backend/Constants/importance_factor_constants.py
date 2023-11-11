from enum import Enum


class WindImportanceFactor(Enum):
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.15
    ULS_POST_DISASTER: float = 1.25
    SLS_LOW: float = 0.75
    SLS_NORMAL: float = 0.75
    SLS_HIGH: float = 0.75
    SLS_POST_DISASTER: float = 0.75


class SnowImportanceFactor(Enum):
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.15
    ULS_POST_DISASTER: float = 1.25
    SLS_LOW: float = 0.9
    SLS_NORMAL: float = 0.9
    SLS_HIGH: float = 0.9
    SLS_POST_DISASTER: float = 0.9


class SeismicImportanceFactor(Enum):
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.3
    ULS_POST_DISASTER: float = 1.5
    SLS_LOW: float = 0.8
    SLS_NORMAL: float = 1
    SLS_HIGH: float = 1.3
    SLS_POST_DISASTER: float = 1.5
