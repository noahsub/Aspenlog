########################################################################################################################
# wind_factor.py
# This file contains classes that represent the wind factor.
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

from backend.Constants.wind_constants import GUST_FACTOR


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class WindFactor:
    """
    This class is used to store the wind factor information
    """

    # Topographic factor
    ct: Optional[float]
    # Exposure factor
    ce: Optional[float]
    cei: Optional[float]
    # Gust factor
    cg: Optional[float]

    def __init__(self):
        """
        Constructor for the WindFactor class
        """
        # Set the attributes
        self.ct = None
        self.ce = None
        self.cei = None
        self.cg = None

    def __str__(self):
        """
        Returns a string representation of the WindFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (
            f"ct: {self.ct}\n" f"ce: {self.ce}\n" f"cei: {self.cei}\n" f"cg: {self.cg}"
        )


class WindFactorBuilderInterface:
    """
    Builder interface for the WindFactor class
    """

    def reset(self):
        pass

    def set_ct(self, ct: float):
        pass

    def set_ce(self, ce: float):
        pass

    def set_cei(self, cei: float):
        pass

    def set_cg(self, cg: float = GUST_FACTOR):
        pass

    def get_ct(self) -> float:
        pass

    def get_ce(self) -> float:
        pass

    def get_cei(self) -> float:
        pass

    def get_cg(self) -> float:
        pass


########################################################################################################################
# BUILDER CLASS
########################################################################################################################


class WindFactorBuilder(WindFactorBuilderInterface):
    """
    Concrete builder class for the WindFactor class
    """

    wind_factor: WindFactor

    def __init__(self):
        """
        Constructor for the WindFactorBuilder class
        """
        # Create a new WindFactor object
        self.reset()

    def reset(self):
        """
        Resets the WindFactorBuilder object
        :return:
        """
        # Create a new WindFactor object
        self.wind_factor = WindFactor()

    def set_ct(self, ct: float):
        """
        Sets the topographic factor
        :param ct: The topographic factor
        :return:
        """
        # Set the topographic factor
        self.wind_factor.ct = ct

    def set_ce(self, ce: float):
        """
        Sets the exposure factor
        :param ce: The exposure factor
        :return:
        """
        # Set the exposure factor
        self.wind_factor.ce = ce

    def set_cei(self, cei: float):
        """
        Sets the exposure factor
        :param cei: The exposure factor
        :return:
        """
        # Set the exposure factor
        self.wind_factor.cei = cei

    def set_cg(self, cg: float = GUST_FACTOR):
        """
        Sets the gust factor
        :param cg: The gust factor
        :return:
        """
        # Set the gust factor
        self.wind_factor.cg = cg

    def get_ct(self) -> float:
        """
        Returns the topographic factor
        :return: The topographic factor
        """
        # Return the topographic factor
        return self.wind_factor.ct

    def get_ce(self) -> float:
        """
        Returns the exposure factor
        :return: The exposure factor
        """
        # Return the exposure factor
        return self.wind_factor.ce

    def get_cei(self) -> float:
        """
        Returns the exposure factor
        :return: The exposure factor
        """
        # Return the exposure factor
        return self.wind_factor.cei

    def get_cg(self) -> float:
        """
        Returns the gust factor
        :return: The gust factor
        """
        # Return the gust factor
        return self.wind_factor.cg

    def get_wind_factor(self) -> WindFactor:
        """
        Returns the WindFactor object and resets the WindFactorBuilder object
        :return: The WindFactor object
        """
        wind_factor = self.wind_factor
        self.reset()
        return wind_factor


class WindFactorDirector:
    @staticmethod
    def construct_wind_factor(builder: WindFactorBuilderInterface):
        raise NotImplementedError
