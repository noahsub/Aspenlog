from typing import Optional

from backend.Entities.Snow.snow_factor import SnowFactor


class SnowLoad:
    """
    This class is used to store all the information regarding snow loads
    """
    # The snow factor
    factor: Optional[SnowFactor]
    # The snow load
    s: Optional[float]

    def __init__(self):
        # Set the attributes
        self.factor = None
        self.s = None

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

