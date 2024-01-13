from typing import Optional

from backend.Entities.Wind.wind_factor import WindFactor
from backend.Entities.Wind.wind_pressure import WindPressure
from backend.Entities.Wind.zone import Zone


class WindLoad:
    """
    This class is used to store all the information regarding wind loads
    """
    # The wind factor
    factor: Optional[WindFactor]
    # The wind pressure
    pressure: Optional[WindPressure]
    # The zones
    zones: Optional[set[Zone]]

    def __init__(self):
        # Set the attributes
        self.factor = None
        self.pressure = None
        # Set the zones
        self.zones = None

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


class WindLoadBuilderInterface:
    """
    Builder interface for the WindLoad class
    """

    def reset(self):
        pass

    def set_factor(self, factor: WindFactor):
        pass

    def set_pressure(self, pressure: WindPressure):
        pass

    def set_zones(self, zones: set[Zone]):
        pass

    def get_factor(self) -> WindFactor:
        pass

    def get_pressure(self) -> WindPressure:
        pass

    def get_zones(self) -> set[Zone]:
        pass


class WindLoadBuilder(WindLoadBuilderInterface):
    """
    Concrete builder class for the WindLoad class
    """
    wind_load: WindLoad

    def __init__(self):
        """
        Constructor for the WindLoadBuilder class
        """
        self.reset()

    def reset(self):
        self.wind_load = WindLoad()

    def set_factor(self, factor: WindFactor):
        self.wind_load.factor = factor

    def set_pressure(self, pressure: WindPressure):
        self.wind_load.pressure = pressure

    def set_zones(self, zones: set[Zone]):
        self.wind_load.zones = zones

    def get_factor(self) -> WindFactor:
        return self.wind_load.factor

    def get_pressure(self) -> WindPressure:
        return self.wind_load.pressure

    def get_zones(self) -> set[Zone]:
        return self.wind_load.zones

    def get_wind_load(self):
        wind_load = self.wind_load
        self.reset()
        return wind_load


class WindLoadDirector:
    @staticmethod
    def construct_snow_factor(builder: WindLoadBuilderInterface):
        raise NotImplementedError
