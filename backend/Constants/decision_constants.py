########################################################################################################################
# decision_constants.py
# This file contains the constants and enums pertaining to the decision-making process
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

class DefaultSelections(Enum):
    """
    Enum for the default selections
    """
    # Default choice
    DEFAULT: str = 'default'
    # Custom choice
    CUSTOM: str = 'custom'
