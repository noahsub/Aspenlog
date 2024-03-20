########################################################################################################################
# seismic_factor.py
# This file contains classes that represent the seismic factor of a building.
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

class SeismicFactor:
    """
    This class is used to store the seismic factor information
    """
    # Element or component force amplification factor
    ar: Optional[float]
    # Element of component response modification factor
    rp: Optional[float]
    # Element of component factor
    cp: Optional[float]

    def __init__(self):
        # Set the attributes
        self.ar = None
        self.rp = None
        self.cp = None

    def __str__(self):
        """
        Returns a string representation of the SeismicFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"ar: {self.ar}\n"
                f"rp: {self.rp}\n"
                f"cp: {self.cp}")


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################

class SeismicFactorBuilderInterface:
    """
    Builder interface for the SeismicFactor class
    """

    def reset(self) -> None:
        pass

    def set_ar(self, ar: float) -> None:
        pass

    def set_rp(self, rp: float) -> None:
        pass

    def set_cp(self, cp: float) -> None:
        pass

    def get_ar(self) -> float:
        pass

    def get_rp(self) -> float:
        pass

    def get_cp(self) -> float:
        pass


class SeismicFactorBuilder(SeismicFactorBuilderInterface):
    """
    Concrete builder class for the SeismicFactor class
    """
    seismic_factor: SeismicFactor

    def __init__(self):
        """
        Constructor for the SeismicFactorBuilder class
        """
        self.reset()

    def reset(self):
        """
        Resets the SeismicFactorBuilder object
        :return: None
        """
        self.seismic_factor = SeismicFactor()

    def set_ar(self, ar: float = 1):
        """
        Sets the ar attribute of the SeismicFactor object
        :param ar: The force amplification factor
        :return: None
        """
        self.seismic_factor.ar = ar

    def set_rp(self, rp: float = 2.5):
        """
        Sets the rp attribute of the SeismicFactor object
        :param rp: The response modification factor
        :return: None
        """
        self.seismic_factor.rp = rp

    def set_cp(self, cp: float = 1):
        """
        Sets the cp attribute of the SeismicFactor object
        :param cp: The component factor
        :return: None
        """
        self.seismic_factor.cp = cp

    def get_ar(self) -> float:
        """
        Returns the ar attribute of the SeismicFactor object
        :return: The force amplification factor
        """
        return self.seismic_factor.ar

    def get_rp(self) -> float:
        """
        Returns the rp attribute of the SeismicFactor object
        :return: The response modification factor
        """
        return self.seismic_factor.rp

    def get_cp(self) -> float:
        """
        Returns the cp attribute of the SeismicFactor object
        :return: The component factor
        """
        return self.seismic_factor.cp

    def get_seismic_factor(self) -> SeismicFactor:
        """
        Returns the SeismicFactor object and resets the builder object to its initial state so that it can be used
        again.
        :return: The constructed SeismicFactor object.
        """
        seismic_factor = self.seismic_factor
        self.reset()
        return seismic_factor


class SeismicFactorDirector:
    @staticmethod
    def construct_seismic_factor(builder: SeismicFactorBuilderInterface):
        raise NotImplementedError
