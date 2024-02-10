########################################################################################################################
# seismic_constants.py
# This file contains the constants and enums pertaining to seismic
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from enum import Enum


########################################################################################################################
# ENUMS
########################################################################################################################

class SiteClass(Enum):
    """
    Enum for the site classes
    """
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

    @staticmethod
    def get_key_from_value(value):
        match value:
            case 'A':
                return SiteClass.A
            case 'B':
                return SiteClass.B
            case 'C':
                return SiteClass.C
            case 'D':
                return SiteClass.D
            case 'E':
                return SiteClass.E


class SiteDesignation(Enum):
    """
    Enum for the site designations
    """
    XV = 'xv'
    XS = 'xs'

    @staticmethod
    def get_key_from_value(value):
        match value:
            case 'xv':
                return SiteDesignation.XV
            case 'xs':
                return SiteDesignation.XS


