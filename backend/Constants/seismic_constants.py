########################################################################################################################
# seismic_constants.py
# This file contains the constants and enums pertaining to seismic
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
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


