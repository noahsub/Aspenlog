from typing import Optional

from backend.Constants.snow_constants import ACCUMULATION_FACTOR


class SnowFactor:
    # Slope factor
    cs: Optional[float]
    # Accumulation factor
    ca: Optional[float]
    # Wind exposure factor
    cw: Optional[float]
    # Basic roof snow load factor
    cb: Optional[float]

    def __init__(self):
        # Set the attributes
        self.cs = None
        self.ca = None
        self.cw = None
        self.cb = None

    def __str__(self):
        """
        Returns a string representation of the SnowFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"cs: {self.cs}\n"
                f"ca: {self.ca}\n"
                f"cw: {self.cw}\n"
                f"cb: {self.cb}")


class SnowFactorBuilderInterface:
    """
    Builder interface for the SnowFactor class
    """

    def reset(self):
        pass

    def set_cs(self, cs: float):
        pass

    def set_ca(self, ca: float):
        pass

    def set_cw(self, cw: float):
        pass

    def set_cb(self, cb: float):
        pass

    def get_cs(self) -> float:
        pass

    def get_ca(self) -> float:
        pass

    def get_cw(self) -> float:
        pass

    def get_cb(self) -> float:
        pass


class SnowFactorBuilder(SnowFactorBuilderInterface):
    """
    Concrete builder class for the SnowFactor class
    """
    snow_factor: SnowFactor

    def __init__(self):
        self.reset()

    def reset(self):
        self.snow_factor = SnowFactor()

    def set_cs(self, cs: float):
        self.snow_factor.cs = cs

    def set_ca(self, ca: float = ACCUMULATION_FACTOR):
        self.snow_factor.ca = ca

    def set_cw(self, cw: float):
        self.snow_factor.cw = cw

    def set_cb(self, cb: float):
        self.snow_factor.cb = cb

    def get_cs(self) -> float:
        return self.snow_factor.cs

    def get_ca(self) -> float:
        return self.snow_factor.ca

    def get_cw(self) -> float:
        return self.snow_factor.cw

    def get_cb(self) -> float:
        return self.snow_factor.cb

    def get_snow_factor(self):
        snow_factor = self.snow_factor
        self.reset()
        return snow_factor


class SnowFactorDirector:
    @staticmethod
    def construct_snow_factor(builder: SnowFactorBuilderInterface):
        raise NotImplementedError
