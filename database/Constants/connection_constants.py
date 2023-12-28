########################################################################################################################
# connection_constants.py
# This file contains the constants and enums pertaining to the connection of a database
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
# ######################################################################################################################

class PrivilegeType(Enum):
    """
    Enum for the privilege types
    """
    ADMIN: str = 'admin'
    WRITE: str = 'write'
    READ: str = 'read'
