from typing import Optional

from backend.Entities.Seismic.seismic_load import SeismicLoad
from backend.Entities.Wind.wind_load import WindLoad


class HeightZone:
    """
    Represents a height zone of a building
    """
    # Number of the height zone
    zone_num: int
    # Elevation of the height zone
    elevation: float
    wind_load: Optional[WindLoad]
    seismic_load: Optional[SeismicLoad]

    def __init__(self, zone_num: int, elevation: float):
        self.zone_num = zone_num
        self.elevation = elevation
        self.wind_load = None
        self.seismic_load = None

    def __str__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n"
                f"wind_load: {str(self.wind_load)}\n"
                f"seismic_load: {str(self.seismic_load)}")

    def __repr__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n"
                f"wind_load: {str(self.wind_load)}\n"
                f"seismic_load: {str(self.seismic_load)}")
