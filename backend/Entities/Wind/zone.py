########################################################################################################################
# wind_pressure.py
# This file contains classes that represent the wind pressure.
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

from backend.Entities.Wind.wind_pressure import WindPressure


########################################################################################################################
# MAIN CLASS
########################################################################################################################

class Zone:
    """
    This class is used to store the zone information
    """
    # The name of the zone
    name: Optional[str]
    # The zone number
    num: Optional[int]
    # The wind pressure
    pressure: Optional[WindPressure]

    def __init__(self):
        """
        Constructor for the Zone class
        :param name: The name of the zone
        :param num: The zone number
        :param pressure: The wind pressure
        :param wind_load: The wind load
        """
        # Set the attributes
        self.name = None
        self.num = None
        self.pressure = None
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
                f"pressure: {self.pressure}\n")


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class ZoneBuilderInterface:
    """
    Builder interface for the Zone class
    """
    def reset(self):
        pass

    def set_name(self, name: str):
        pass

    def set_num(self, num: int):
        pass

    def set_pressure(self, pressure: WindPressure):
        pass

    def get_name(self) -> str:
        pass

    def get_num(self) -> int:
        pass

    def get_pressure(self) -> WindPressure:
        pass


class ZoneBuilder(ZoneBuilderInterface):
    zone: Zone

    def __init__(self):
        """
        Constructor for the ZoneBuilder class
        """
        self.reset()

    def reset(self):
        """
        Resets the builder
        :return: None
        """
        self.zone = Zone()

    def set_name(self, name: str):
        """
        Sets the name of the zone
        :param name: The name of the zone
        :return: None
        """
        self.zone.name = name

    def set_num(self, num: int):
        """
        Sets the number of the zone
        :param num: The number of the zone
        :return: None
        """
        self.zone.num = num

    def set_pressure(self, pressure: WindPressure):
        """
        Sets the wind pressure of the zone
        :param pressure: The wind pressure of the zone
        :return: None
        """
        self.zone.pressure = pressure

    def get_name(self) -> str:
        """
        Gets the name of the zone
        :return: The name of the zone
        """
        return self.zone.name

    def get_num(self) -> int:
        """
        Gets the number of the zone
        :return: The number of the zone
        """
        return self.zone.num

    def get_pressure(self) -> WindPressure:
        """
        Gets the wind pressure of the zone
        :return: The wind pressure of the zone
        """
        return self.zone.pressure

    def get_zone(self):
        """
        Gets the zone and resets the builder
        :return: The zone
        """
        zone = self.zone
        self.reset()
        return zone


class ZoneDirector:
    @staticmethod
    def construct_snow_factor(builder: ZoneBuilderInterface):
        raise NotImplementedError
