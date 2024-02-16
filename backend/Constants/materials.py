########################################################################################################################
# DEPRECIATED
########################################################################################################################
# materials.py
# This file contains the constants and enums pertaining to materials
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

class Materials(Enum):
    """
    Enum for the materials
    """
    GLASS = 'glass'
    GRANITE = 'granite'
    SANDSTONE = 'sandstone'
    STEEL = 'steel'
    OTHER = 'other'

    @classmethod
    def get_materials_list(cls):
        """
        Gets a list of the materials
        :return: A list of the materials according to their name rather than value
        """
        materials_list = []
        for material in cls:
            materials_list.append(material.name)
        return materials_list
