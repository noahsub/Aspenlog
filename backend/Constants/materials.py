########################################################################################################################
# DEPRECIATED
########################################################################################################################
# materials.py
# This file contains the constants and enums pertaining to materials
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


class Materials(Enum):
    """
    Enum for the materials
    """

    GLASS = "glass"
    GRANITE = "granite"
    SANDSTONE = "sandstone"
    STEEL = "steel"
    OTHER = "other"

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
