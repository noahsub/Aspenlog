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


class SnowLoadBuilderInterface:
    def reset(self):
        pass

    def set_factor(self, factor: SnowFactor) -> None:
        pass

    def set_s(self, s: float) -> None:
        pass

    def get_factor(self) -> SnowFactor:
        pass

    def get_s(self) -> float:
        pass


class SnowLoadBuilder(SnowLoadBuilderInterface):
    snow_load: SnowLoad

    def __init__(self):
        self.reset()

    def reset(self):
        self.snow_load = SnowLoad()

    def set_factor(self, factor: SnowFactor) -> None:
        self.snow_load.factor = factor

    def set_s(self, s: float) -> None:
        self.snow_load.s = s

    def get_factor(self) -> SnowFactor:
        return self.snow_load.factor

    def get_s(self) -> float:
        return self.snow_load.s

    def get_snow_load(self) -> SnowLoad:
        snow_load = self.snow_load
        self.reset()
        return snow_load


class SnowLoadDirector:
    @staticmethod
    def construct_snow_load(builder: SnowLoadBuilderInterface):
        raise NotImplementedError
