from typing import Optional

from backend.Entities.Snow.snow_factor import SnowFactor


class SnowLoad:
    """
    This class is used to store all the information regarding snow loads
    """
    # The snow factor
    factor: Optional[SnowFactor]
    # The snow load
    s_uls: Optional[float]

    def __init__(self):
        # Set the attributes
        self.factor = None
        self.s_uls = None
        self.s_sls = None

    def __str__(self):
        """
        Returns a string representation of the SnowLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))

        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"s: {self.s_uls}\n"
                f"s: {self.s_sls}")


class SnowLoadBuilderInterface:
    def reset(self):
        pass

    def set_factor(self, factor: SnowFactor) -> None:
        pass

    def set_s_uls(self, s_uls: float) -> None:
        pass

    def set_s_sls(self, s_sls: float) -> None:
        pass

    def get_factor(self) -> SnowFactor:
        pass

    def get_s_uls(self) -> float:
        pass

    def get_s_sls(self) -> float:
        pass


class SnowLoadBuilder(SnowLoadBuilderInterface):
    snow_load: SnowLoad

    def __init__(self):
        self.reset()

    def reset(self):
        self.snow_load = SnowLoad()

    def set_factor(self, factor: SnowFactor) -> None:
        self.snow_load.factor = factor

    def set_s_uls(self, s: float) -> None:
        self.snow_load.s_uls = s

    def set_s_sls(self, s: float) -> None:
        self.snow_load.s_sls = s

    def get_factor(self) -> SnowFactor:
        return self.snow_load.factor

    def get_s_uls(self) -> float:
        return self.snow_load.s_uls

    def get_s_sls(self) -> float:
        return self.snow_load.s_sls

    def get_snow_load(self) -> SnowLoad:
        snow_load = self.snow_load
        self.reset()
        return snow_load


class SnowLoadDirector:
    @staticmethod
    def construct_snow_load(builder: SnowLoadBuilderInterface):
        raise NotImplementedError
