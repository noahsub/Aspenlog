from typing import Optional

from backend.Entities.Wind.wind_pressure import WindPressure


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
    # TODO: IMPLEMENT ZONE WIDTH

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
        self.reset()

    def reset(self):
        self.zone = Zone()

    def set_name(self, name: str):
        self.zone.name = name

    def set_num(self, num: int):
        self.zone.num = num

    def set_pressure(self, pressure: WindPressure):
        self.zone.pressure = pressure

    def get_name(self) -> str:
        return self.zone.name

    def get_num(self) -> int:
        return self.zone.num

    def get_pressure(self) -> WindPressure:
        return self.zone.pressure

    def get_zone(self):
        zone = self.zone
        self.reset()
        return zone


class ZoneDirector:
    @staticmethod
    def construct_snow_factor(builder: ZoneBuilderInterface):
        raise NotImplementedError
