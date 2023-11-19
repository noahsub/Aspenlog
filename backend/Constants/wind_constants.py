from enum import Enum


class WindExposureFactorSelections(Enum):
    OPEN: str = 'open'
    ROUGH: str = 'rough'
    INTERMEDIATE: str = 'intermediate'


class InternalPressureSelections(Enum):
    ENCLOSED: str = 'enclosed'
    PARTIALLY_ENCLOSED: str = 'partially_enclosed'
    LARGE_OPENINGS: str = 'large_openings'

