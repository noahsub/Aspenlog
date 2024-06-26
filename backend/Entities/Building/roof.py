########################################################################################################################
# roof.py
# This file contains classes that represent the roof of a building.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from typing import Optional


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class Roof:
    """
    Represents the roof of a building
    """

    # Smaller Plan dimension of the roof (m)
    w_roof: Optional[float]
    # Larger Plan dimension of the roof (m)
    l_roof: Optional[float]
    # Slope of the roof (degrees)
    slope: Optional[float]
    # Wall slope of the roof
    wall_slope: Optional[int]
    # Uniform dead load for roof (kPa)
    wp: Optional[float]

    def __init__(self):
        """
        Constructor for Roof class
        """
        self.w_roof = None
        self.l_roof = None
        self.slope = None
        self.wall_slope = None
        self.wp = None

    def __str__(self):
        """
        String representation of the Roof class
        :return:
        """
        # Print each attribute and its value on a new line
        return (
            f"w_roof: {self.w_roof}\n"
            f"l_roof: {self.l_roof}\n"
            f"slope: {self.slope}\n"
            f"wall_slope: {self.wall_slope}\n"
            f"wp: {self.wp}"
        )


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class RoofBuilderInterface:
    """
    Builder interface for the Cladding class
    """

    def reset(self):
        pass

    def set_w_roof(self, w_roof: float):
        pass

    def set_l_roof(self, l_roof: float):
        pass

    def set_slope(self, slope: float):
        pass

    def compute_wall_slope(self):
        pass

    def set_wp(self, wp: float):
        pass

    def get_w_roof(self) -> float:
        pass

    def get_l_roof(self) -> float:
        pass

    def get_slope(self) -> float:
        pass

    def get_wall_slope(self) -> float:
        pass

    def get_wp(self) -> float:
        pass


class RoofBuilder(RoofBuilderInterface):
    """
    Concrete builder class for the Cladding class
    """

    roof: Roof

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.roof = Roof()

    def set_w_roof(self, w_roof: float):
        self.roof.w_roof = w_roof

    def set_l_roof(self, l_roof: float):
        self.roof.l_roof = l_roof

    def set_slope(self, slope: float):
        self.roof.slope = slope

    def compute_wall_slope(self):
        assert self.roof.slope is not None
        if 30 <= self.roof.slope <= 70:
            self.roof.wall_slope = 1
        else:
            self.roof.wall_slope = 0

    def set_wp(self, wp: float):
        self.roof.wp = wp

    def get_w_roof(self):
        return self.roof.w_roof

    def get_l_roof(self):
        return self.roof.l_roof

    def get_slope(self):
        return self.roof.slope

    def get_wall_slope(self):
        return self.roof.wall_slope

    def get_wp(self):
        return self.roof.wp

    def get_roof(self):
        """
        Returns the roof object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed roof object.
        """
        roof = self.roof
        self.reset()
        return roof


class RoofDirector:
    @staticmethod
    def construct_roof(builder: RoofBuilderInterface):
        raise NotImplementedError
