########################################################################################################################
# seismic.py
# This file contains the SeismicLoad class and associated subclasses, which are used to store all the information
# regarding seismic loads
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# SUBCLASSES
########################################################################################################################

class SeismicFactor:
    """
    This class is used to store the seismic factor information
    """
    # Element or component force amplification factor
    ar: float
    # Element of component response modification factor
    rp: float
    # Element of component factor
    cp: float

    def __init__(self, ar: float = 1, rp: float = 2.5, cp: float = 1):
        """
        Constructor for the SeismicFactor class
        :param ar: Element or component force amplification factor
        :param rp: Element of component response modification factor
        :param cp: Element of component factor
        """
        # Set the attributes
        self.ar = ar
        self.rp = rp
        self.cp = cp

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
# MAIN CLASS
########################################################################################################################

class SeismicLoad:
    """
    This class is used to store all the information regarding seismic loads
    """
    # The seismic factor
    factor: SeismicFactor
    # Height factor
    ax: float
    # Horizontal force factor for the part or portion of the building
    sp: float
    # Specified lateral earthquake force
    vp: float
    vp_snow: float

    def __init__(self, factor: SeismicFactor, ax: float, sp: float, vp: float, vp_snow: float):
        """
        Constructor for the SeismicLoad class
        :param factor: The seismic factor
        :param ax: Height factor
        :param sp: Horizontal force factor for the part or portion of the building
        :param vp: Specified lateral earthquake force
        :param vp_snow: Specified lateral earthquake force for snow
        """
        # Assign the attributes
        self.factor = factor
        self.ax = ax
        self.sp = sp
        self.vp = vp
        self.vp_snow = vp_snow

    def __str__(self):
        """
        Returns a string representation of the SeismicLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))
        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"ax: {self.ax}\n"
                f"sp: {self.sp}\n"
                f"vp: {self.vp}\n"
                f"vp_snow: {self.vp_snow}")
