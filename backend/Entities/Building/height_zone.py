from typing import Optional, Dict

from backend.Constants.materials import Materials


class HeightZone:
    """
    Represents a height zone of a building
    """
    # Number of the height zone
    zone_num: int
    # Elevation of the height zone
    elevation: float
    # Material percentages for the height zone
    wp_materials: Optional[Dict[Materials, float]]

    def __init__(self):
        self.zone_num = None
        self.elevation = None
        self.wp_materials = None

    def __str__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n,"
                f"wp_materials: {self.wp_materials}")


class HeightZoneBuilderInterface:
    """
    Builder interface for the HeightZone class
    """

    def reset(self) -> None:
        pass

    def set_zone_num(self, zone_num: int) -> None:
        pass

    def set_elevation(self, elevation: float) -> None:
        pass

    def set_wp_materials(self, wp_materials: Dict[Materials, float]) -> None:
        pass

    def get_zone_num(self) -> int:
        pass

    def get_elevation(self) -> float:
        pass

    def get_wp_materials(self) -> Dict[Materials, float]:
        pass


class HeightZoneBuilder(HeightZoneBuilderInterface):
    """
    Concrete builder class for the HeightZone class
    """
    height_zone: HeightZone

    def __init__(self):
        self.reset()

    def reset(self):
        self.height_zone = HeightZone()

    def set_zone_num(self, zone_num: int):
        self.height_zone.zone_num = zone_num

    def set_elevation(self, elevation: float):
        self.height_zone.elevation = elevation

    def set_wp_materials(self, wp_materials: Dict[Materials, float]):
        self.height_zone.wp_materials = wp_materials

    def get_zone_num(self) -> int:
        return self.height_zone.zone_num

    def get_elevation(self) -> float:
        return self.height_zone.elevation

    def get_wp_materials(self) -> Dict[Materials, float]:
        return self.height_zone.wp_materials

    def get_height_zone(self) -> HeightZone:
        height_zone = self.height_zone
        self.reset()
        return height_zone


class HeightZoneDirector:
    @staticmethod
    def construct_height_zone(builder: HeightZoneBuilderInterface) -> None:
        raise NotImplementedError
