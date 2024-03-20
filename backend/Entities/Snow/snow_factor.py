########################################################################################################################
# snow_factor.py
# This file contains classes that represent the snow factor of a building.
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

from backend.Constants.snow_constants import ACCUMULATION_FACTOR


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class SnowFactor:
    # Slope factor
    cs: Optional[float]
    # Accumulation factor
    ca: Optional[float]
    # Wind exposure factor
    cw: Optional[float]
    # Basic roof snow load factor
    cb: Optional[float]

    def __init__(self):
        # Set the attributes
        self.cs = None
        self.ca = None
        self.cw = None
        self.cb = None

    def __str__(self):
        """
        Returns a string representation of the SnowFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return f"cs: {self.cs}\n" f"ca: {self.ca}\n" f"cw: {self.cw}\n" f"cb: {self.cb}"


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class SnowFactorBuilderInterface:
    """
    Builder interface for the SnowFactor class
    """

    def reset(self):
        pass

    def set_cs(self, cs: float):
        pass

    def set_ca(self, ca: float):
        pass

    def set_cw(self, cw: float):
        pass

    def set_cb(self, cb: float):
        pass

    def get_cs(self) -> float:
        pass

    def get_ca(self) -> float:
        pass

    def get_cw(self) -> float:
        pass

    def get_cb(self) -> float:
        pass


class SnowFactorBuilder(SnowFactorBuilderInterface):
    """
    Concrete builder class for the SnowFactor class
    """

    snow_factor: SnowFactor

    def __init__(self):
        """
        Initialize the builder
        """
        self.reset()

    def reset(self):
        """
        Reset the builder
        :return: None
        """
        self.snow_factor = SnowFactor()

    def set_cs(self, cs: float):
        """
        Set the slope factor
        :param cs: The slope factor
        :return: None
        """
        self.snow_factor.cs = cs

    def set_ca(self, ca: float = ACCUMULATION_FACTOR):
        """
        Set the accumulation factor
        :param ca: The accumulation factor
        :return: None
        """
        self.snow_factor.ca = ca

    def set_cw(self, cw: float):
        """
        Set the wind exposure factor
        :param cw: The wind exposure factor
        :return: None
        """
        self.snow_factor.cw = cw

    def set_cb(self, cb: float):
        """
        Set the basic roof snow load factor
        :param cb: The basic roof snow load factor
        :return: None
        """
        self.snow_factor.cb = cb

    def get_cs(self) -> float:
        """
        Get the slope factor
        :return: The slope factor
        """
        return self.snow_factor.cs

    def get_ca(self) -> float:
        """
        Get the accumulation factor
        :return: The accumulation factor
        """
        return self.snow_factor.ca

    def get_cw(self) -> float:
        """
        Get the wind exposure factor
        :return: The wind exposure factor
        """
        return self.snow_factor.cw

    def get_cb(self) -> float:
        """
        Get the basic roof snow load factor
        :return: The basic roof snow load factor
        """
        return self.snow_factor.cb

    def get_snow_factor(self):
        """
        Get the snow factor
        :return: The snow factor
        """
        snow_factor = self.snow_factor
        self.reset()
        return snow_factor


class SnowFactorDirector:
    @staticmethod
    def construct_snow_factor(builder: SnowFactorBuilderInterface):
        raise NotImplementedError
