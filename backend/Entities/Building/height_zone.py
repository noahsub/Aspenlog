class HeightZone:
    """
    Represents a height zone of a building
    """
    # Number of the height zone
    zone_num: int
    # Elevation of the height zone
    elevation: float

    def __init__(self, zone_num: int, elevation: float):
        self.zone_num = zone_num
        self.elevation = elevation

    def __str__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n")

    def __repr__(self):
        """
        String representation of the HeightZone class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"zone_num: {self.zone_num}\n,"
                f"elevation: {self.elevation}\n")
