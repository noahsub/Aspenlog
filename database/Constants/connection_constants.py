########################################################################################################################
# connection_constants.py
# This file contains the constants and enums pertaining to the connection of a database
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

class PrivilegeType(Enum):
    """
    Enum for the privilege types
    """
    ADMIN: str = 'admin'
    WRITE: str = 'write'
    READ: str = 'read'
