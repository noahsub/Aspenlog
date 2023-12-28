########################################################################################################################
# snow.py
# This file contains the SnowLoad class and associated subclasses, which are used to store all the information
# regarding snow loads
# 
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.snow_constants import ACCUMULATION_FACTOR


########################################################################################################################
# SUBCLASSES
########################################################################################################################

class SnowFactor:
    # Slope factor
    cs: float
    # Accumulation factor
    ca: float
    # Wind exposure factor
    cw: float
    # Basic roof snow load factor
    cb: float

    def __init__(self, cs: float, cw: float, cb: float):
        """
        Constructor for the SnowFactor class
        :param cs: Slope factor
        :param cw: Wind exposure factor
        :param cb: Basic roof snow load factor
        """
        # Set the attributes
        self.cs = cs
        self.ca = ACCUMULATION_FACTOR
        self.cw = cw
        self.cb = cb

    def __str__(self):
        """
        Returns a string representation of the SnowFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"cs: {self.cs}\n"
                f"ca: {self.ca}\n"
                f"cw: {self.cw}\n"
                f"cb: {self.cb}")

########################################################################################################################
# MAIN CLASS
########################################################################################################################


class SnowLoad:
    """
    This class is used to store all the information regarding snow loads
    """
    # The snow factor
    factor: SnowFactor
    # The snow load
    s: float

    def __init__(self, factor: SnowFactor, s: float):
        """
        Constructor for the SnowLoad class
        :param factor: The snow factor
        :param s: The snow load
        """
        # Set the attributes
        self.factor = factor
        self.s = s

    def __str__(self):
        """
        Returns a string representation of the SnowLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))

        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"s: {self.s}")
