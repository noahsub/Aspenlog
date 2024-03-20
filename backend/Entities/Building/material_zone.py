########################################################################################################################
# material_zone.py
# This file contains classes that represent the material zones of a building.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from typing import List

from backend.Constants.materials import Materials


########################################################################################################################
# HELPER CLASS
########################################################################################################################


class MaterialComposition:
    material: Materials
    respected_percentage: float
    weight: float

    def __init__(self, material: Materials, respected_percentage: float, weight: float):
        self.material = material
        self.respected_percentage = respected_percentage
        self.weight = weight

    def __str__(self):
        return (
            f"material: {self.material}\n,"
            f"respected percentage: {self.respected_percentage}\n,"
            f"weight: {self.weight}\n"
        )

    def __repr__(self):
        return (
            f"material: {self.material}\n,"
            f"respected percentage: {self.respected_percentage}\n,"
            f"weight: {self.weight}\n"
        )


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class MaterialZone:
    """
    Represents the material composition of a height zone of a building
    """

    materials_list: List[MaterialComposition]

    def __init__(self, materials_list):
        self.materials_list = materials_list

    def __str__(self):
        """
        String representation of the MaterialZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return f"materials list: {[str(x) for x in self.materials_list]}\n"

    def __repr__(self):
        """
        String representation of the MaterialZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return f"materials list: {[str(x) for x in self.materials_list]}\n"
