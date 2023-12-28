########################################################################################################################
# wind.py
# This file contains the WindLoad class and associated subclasses, which are used to store all the information
# regarding wind loads
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.wind_constants import GUST_FACTOR


########################################################################################################################
# SUBCLASSES
########################################################################################################################

class WindFactor:
    """
    This class is used to store the wind factor information
    """
    # Topographic factor
    ct: float
    # Exposure factor
    ce: float
    cei: float
    # Gust factor
    cg: float

    def __init__(self, ct: float, ce: float, cei: float):
        """
        Constructor for the WindFactor class
        :param ct: The topographic factor
        :param ce: The exposure factor
        :param cei: The exposure factor
        """
        # Set the attributes
        self.ct = ct
        self.ce = ce
        self.cei = cei
        self.cg = GUST_FACTOR

    def __str__(self):
        """
        Returns a string representation of the WindFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"ct: {self.ct}\n"
                f"ce: {self.ce}\n"
                f"cei: {self.cei}\n"
                f"cg: {self.cg}")


class WindPressure:
    """
    This class is used to store the wind pressure information
    """
    # Positive internal pressure
    pi_pos: float
    # Negative internal pressure
    pi_neg: float
    # Positive external pressure
    pe_pos: float
    # Negative external pressure
    pe_neg: float

    def __init__(self, pi_pos: float = None, pi_neg: float = None, pe_pos: float = None, pe_neg: float = None):
        """
        Constructor for the WindPressure class
        :param pi_pos: The positive internal pressure
        :param pi_neg: The negative internal pressure
        :param pe_pos: The positive external pressure
        :param pe_neg: The negative external pressure
        """
        # Set the attributes
        self.pi_pos = pi_pos
        self.pi_neg = pi_neg
        self.pe_pos = pe_pos
        self.pe_neg = pe_neg

    def __str__(self):
        """
        Returns a string representation of the WindPressure object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"pi_pos: {self.pi_pos}\n"
                f"pi_neg: {self.pi_neg}\n"
                f"pe_pos: {self.pe_pos}\n"
                f"pe_neg: {self.pe_neg}")


class Zone:
    """
    This class is used to store the zone information
    """
    # The name of the zone
    name: str
    # The zone number
    num: int
    # The wind pressure
    pressure: WindPressure
    # The wind load
    wind_load: float

    def __init__(self, name: str, num: int, pressure: WindPressure, wind_load: float = None):
        """
        Constructor for the Zone class
        :param name: The name of the zone
        :param num: The zone number
        :param pressure: The wind pressure
        :param wind_load: The wind load
        """
        # Set the attributes
        self.name = name
        self.num = num
        self.pressure = pressure
        # Set to None for string representation purposes
        self.wind_load = None

    def __str__(self):
        """
        Returns a string representation of the Zone object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"name: {self.name}\n"
                f"num: {self.num}\n"
                f"pressure: {self.pressure}\n"
                f"wind_load: {self.wind_load}")

########################################################################################################################
# MAIN CLASS
########################################################################################################################


class WindLoad:
    """
    This class is used to store all the information regarding wind loads
    """
    # The wind factor
    factor: WindFactor
    # The wind pressure
    pressure: WindPressure
    # The zones
    zones: set[Zone]

    def __init__(self, factor: WindFactor, pressure: WindPressure):
        # Set the attributes
        self.factor = factor
        self.pressure = pressure
        # Set the zones
        self.zones = {
            Zone('roof_interior', 1, WindPressure()),
            Zone('roof_edge', 2, WindPressure()),
            Zone('roof_corner', 3, WindPressure()),
            Zone('wall_centre', 4, WindPressure()),
            Zone('wall_corner', 5, WindPressure())
        }

    def get_zone(self, key):
        """
        Function to get a zone by name or number
        :param key: The name or number of the zone
        :return:
        """
        # If the key is a string, search by name
        if type(key) == str:
            for zone in self.zones:
                if zone.name == key:
                    return zone
        # If the key is an int, search by number
        elif type(key) == int:
            for zone in self.zones:
                if zone.num == key:
                    return zone

    def __str__(self):
        """
        Returns a string representation of the WindLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))
        pressure_str = '\n  ' + '\n  '.join(str(self.pressure).split('\n'))

        # Special formatting for zones
        zones_str = '\n'
        for zone in self.zones:
            zones_str += f"  zone {zone.num}\n"
            zone_lst = str(zone).split('\n')
            for i in zone_lst:
                zones_str += f"    {i.lstrip(', ')}\n"
        zones_str = zones_str[:-1]

        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"pressure: {pressure_str}\n"
                f"zones: {zones_str}")
