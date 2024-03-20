########################################################################################################################
# snow_load.py
# This file contains classes that represent the snow load of a building.
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

from backend.Entities.Snow.snow_factor import SnowFactor


########################################################################################################################
# MAIN CLASS
########################################################################################################################

class SnowLoad:
    """
    This class is used to store all the information regarding snow loads
    """
    # The snow factor
    factor: Optional[SnowFactor]
    # The snow load
    s_uls: Optional[float]

    def __init__(self):
        # Set the attributes
        self.factor = None
        self.s_uls = None
        self.s_sls = None

    def __str__(self):
        """
        Returns a string representation of the SnowLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))

        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"s_uls: {self.s_uls}\n"
                f"s_sls: {self.s_sls}")


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class SnowLoadBuilderInterface:
    def reset(self):
        pass

    def set_factor(self, factor: SnowFactor) -> None:
        pass

    def set_s_uls(self, s_uls: float) -> None:
        pass

    def set_s_sls(self, s_sls: float) -> None:
        pass

    def get_factor(self) -> SnowFactor:
        pass

    def get_s_uls(self) -> float:
        pass

    def get_s_sls(self) -> float:
        pass


class SnowLoadBuilder(SnowLoadBuilderInterface):
    snow_load: SnowLoad

    def __init__(self):
        """
        Initializes the SnowLoadBuilder object
        """
        self.reset()

    def reset(self):
        """
        Resets the snow load
        :return: None
        """
        self.snow_load = SnowLoad()

    def set_factor(self, factor: SnowFactor) -> None:
        """
        Sets the snow factor
        :param factor: The snow factor
        :return: None
        """
        self.snow_load.factor = factor

    def set_s_uls(self, s: float) -> None:
        """
        Sets the snow load for the ultimate limit state
        :param s: The uls snow load
        :return: None
        """
        self.snow_load.s_uls = s

    def set_s_sls(self, s: float) -> None:
        """
        Sets the snow load for the serviceability limit state
        :param s: The sls snow load
        :return: None
        """
        self.snow_load.s_sls = s

    def get_factor(self) -> SnowFactor:
        """
        Returns the snow factor
        :return: The snow factor
        """
        return self.snow_load.factor

    def get_s_uls(self) -> float:
        """
        Returns the snow load for the ultimate limit state
        :return: The uls snow load
        """
        return self.snow_load.s_uls

    def get_s_sls(self) -> float:
        """
        Returns the snow load for the serviceability limit state
        :return: The sls snow load
        """
        return self.snow_load.s_sls

    def get_snow_load(self) -> SnowLoad:
        """
        Returns the snow load and resets the builder
        :return: The snow load
        """
        snow_load = self.snow_load
        self.reset()
        return snow_load


class SnowLoadDirector:
    @staticmethod
    def construct_snow_load(builder: SnowLoadBuilderInterface):
        raise NotImplementedError
