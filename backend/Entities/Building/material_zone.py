from typing import List

from backend.Constants.materials import Materials


class MaterialComposition:
    material: Materials
    respected_percentage: float

    def __init__(self, material: Materials, respected_percentage: float):
        self.material = material
        self.respected_percentage = respected_percentage

    def __str__(self):
        return (f"material: {self.material}\n,"
                f"respected percentage: {self.respected_percentage}\n")


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
        return f"materials list: {self.materials_list}\n"
