########################################################################################################################
# importance_factor_constants.py
# This file contains the constants and enums pertaining to the importance factors
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from enum import Enum

from backend.Constants.load_constants import LoadTypes


########################################################################################################################
# ENUMS
########################################################################################################################

class ImportanceFactor(Enum):
    LOW: str = 'LOW'
    NORMAL: str = 'NORMAL'
    HIGH: str = 'HIGH'
    POST_DISASTER: str = 'POST_DISASTER'

    def get_importance_factor_uls(self, load_type: LoadTypes):
        match self:
            case self.LOW:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.ULS_LOW.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.ULS_LOW.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.ULS_LOW.value
            case self.NORMAL:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.ULS_NORMAL.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.ULS_NORMAL.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.ULS_NORMAL.value
            case self.HIGH:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.ULS_HIGH.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.ULS_HIGH.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.ULS_HIGH.value
            case self.POST_DISASTER:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.ULS_POST_DISASTER.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.ULS_POST_DISASTER.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.ULS_POST_DISASTER.value

    def get_importance_factor_sls(self, load_type: LoadTypes):
        match self:
            case self.LOW:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.SLS_LOW.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.SLS_LOW.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.SLS_LOW.value
            case self.NORMAL:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.SLS_NORMAL.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.SLS_NORMAL.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.SLS_NORMAL.value
            case self.HIGH:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.SLS_HIGH.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.SLS_HIGH.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.SLS_HIGH.value
            case self.POST_DISASTER:
                match load_type:
                    case LoadTypes.WIND:
                        return WindImportanceFactor.SLS_POST_DISASTER.value
                    case LoadTypes.SNOW:
                        return SnowImportanceFactor.SLS_POST_DISASTER.value
                    case LoadTypes.SEISMIC:
                        return SeismicImportanceFactor.SLS_POST_DISASTER.value


class LimitState(Enum):
    ULS: str = 'ULS'
    SLS: str = 'SLS'


class WindImportanceFactor(Enum):
    """
    Enum for the wind importance factors
    """
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.15
    ULS_POST_DISASTER: float = 1.25
    SLS_LOW: float = 0.75
    SLS_NORMAL: float = 0.75
    SLS_HIGH: float = 0.75
    SLS_POST_DISASTER: float = 0.75


class SnowImportanceFactor(Enum):
    """
    Enum for the snow importance factors
    """
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.15
    ULS_POST_DISASTER: float = 1.25
    SLS_LOW: float = 0.9
    SLS_NORMAL: float = 0.9
    SLS_HIGH: float = 0.9
    SLS_POST_DISASTER: float = 0.9


class SeismicImportanceFactor(Enum):
    """
    Enum for the seismic importance factors
    Note: The values for ULS and SLS are the same for seismic
    """
    ULS_LOW: float = 0.8
    ULS_NORMAL: float = 1
    ULS_HIGH: float = 1.3
    ULS_POST_DISASTER: float = 1.5
    SLS_LOW: float = 0.8
    SLS_NORMAL: float = 1
    SLS_HIGH: float = 1.3
    SLS_POST_DISASTER: float = 1.5
