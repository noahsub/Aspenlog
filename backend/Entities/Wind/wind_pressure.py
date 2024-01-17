from typing import Optional


class WindPressure:
    """
    This class is used to store the wind pressure information
    """
    # Positive internal pressure
    pi_pos: Optional[float]
    # Negative internal pressure
    pi_neg: Optional[float]
    # Positive external pressure
    pe_pos: Optional[float]
    # Negative external pressure
    pe_neg: Optional[float]
    # POS value for user display
    pos: Optional[float]
    # NEG value for user display
    neg: Optional[float]

    def __init__(self):
        """
        Constructor for the WindPressure class
        :param pi_pos: The positive internal pressure
        :param pi_neg: The negative internal pressure
        :param pe_pos: The positive external pressure
        :param pe_neg: The negative external pressure
        """
        # Set the attributes
        self.pi_pos = None
        self.pi_neg = None
        self.pe_pos = None
        self.pe_neg = None
        self.pos = None
        self.neg = None

    def __str__(self):
        """
        Returns a string representation of the WindPressure object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"pi_pos: {self.pi_pos}\n"
                f"pi_neg: {self.pi_neg}\n"
                f"pe_pos: {self.pe_pos}\n"
                f"pe_neg: {self.pe_neg}\n"
                f"pos: {self.pos}\n"
                f"neg: {self.neg}")


class WindPressureBuilderInterface:
    """
    Builder interface for the WindPressure class
    """

    def reset(self):
        pass

    def set_pi_pos(self, pi_pos: float):
        pass

    def set_pi_neg(self, pi_neg: float):
        pass

    def set_pe_pos(self, pe_pos: float):
        pass

    def set_pe_neg(self, pe_neg: float):
        pass

    def set_pos(self):
        pass

    def set_neg(self):
        pass

    def get_pi_pos(self) -> float:
        pass

    def get_pi_neg(self) -> float:
        pass

    def get_pe_pos(self) -> float:
        pass

    def get_pe_neg(self) -> float:
        pass

    def get_pos(self) -> float:
        pass

    def get_neg(self) -> float:
        pass


class WindPressureBuilder(WindPressureBuilderInterface):
    """
    Concrete builder class for the WindPressure class
    """
    wind_pressure: WindPressure

    def __init__(self):
        """
        Constructor for the WindPressureBuilder class
        """
        # Create a new WindPressure object
        self.reset()

    def reset(self):
        """
        Resets the WindPressureBuilder object
        :return:
        """
        # Create a new WindPressure object
        self.wind_pressure = WindPressure()

    def set_pi_pos(self, pi_pos: float):
        """
        Sets the positive internal pressure
        :param pi_pos: The positive internal pressure
        :return:
        """
        self.wind_pressure.pi_pos = pi_pos

    def set_pi_neg(self, pi_neg: float):
        """
        Sets the negative internal pressure
        :param pi_neg: The negative internal pressure
        :return:
        """
        self.wind_pressure.pi_neg = pi_neg

    def set_pe_pos(self, pe_pos: float):
        """
        Sets the positive external pressure
        :param pe_pos: The positive external pressure
        :return:
        """
        self.wind_pressure.pe_pos = pe_pos

    def set_pe_neg(self, pe_neg: float):
        """
        Sets the negative external pressure
        :param pe_neg: The negative external pressure
        :return:
        """
        self.wind_pressure.pe_neg = pe_neg

    def set_pos(self):
        assert self.wind_pressure.pe_pos is not None
        assert self.wind_pressure.pi_neg is not None
        self.wind_pressure.pos = self.wind_pressure.pe_pos - self.wind_pressure.pi_neg

    def set_neg(self):
        assert self.wind_pressure.pe_neg is not None
        assert self.wind_pressure.pi_pos is not None
        self.wind_pressure.neg = self.wind_pressure.pe_neg - self.wind_pressure.pi_pos

    def get_pi_pos(self) -> float:
        """
        Returns the positive internal pressure
        :return: The positive internal pressure
        """
        return self.wind_pressure.pi_pos

    def get_pi_neg(self) -> float:
        """
        Returns the negative internal pressure
        :return: The negative internal pressure
        """
        return self.wind_pressure.pi_neg

    def get_pe_pos(self) -> float:
        """
        Returns the positive external pressure
        :return: The positive external pressure
        """
        return self.wind_pressure.pe_pos

    def get_pe_neg(self) -> float:
        """
        Returns the negative external pressure
        :return: The negative external pressure
        """
        return self.wind_pressure.pe_neg

    def get_pos(self) -> float:
        """
        Returns the positive pressure
        :return: The positive pressure
        """
        return self.wind_pressure.pos

    def get_neg(self) -> float:
        """
        Returns the negative pressure
        :return: The negative pressure
        """
        return self.wind_pressure.neg

    def get_wind_pressure(self) -> WindPressure:
        """
        Returns the WindPressure object
        :return: The WindPressure object
        """
        wind_pressure = self.wind_pressure
        self.reset()
        return wind_pressure


class WindPressureDirector:
    @staticmethod
    def construct_snow_factor(builder: WindPressureBuilderInterface):
        raise NotImplementedError
