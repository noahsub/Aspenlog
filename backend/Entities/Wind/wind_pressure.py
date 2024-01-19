from typing import Optional


class WindPressure:
    """
    This class is used to store the wind pressure information
    """
    # Positive internal pressure
    pi_pos_uls: Optional[float]
    # Negative internal pressure
    pi_neg_uls: Optional[float]
    # Positive external pressure
    pe_pos_uls: Optional[float]
    # Negative external pressure
    pe_neg_uls: Optional[float]
    # POS value for user display
    pos_uls: Optional[float]
    # NEG value for user display
    neg_uls: Optional[float]
    # Positive internal pressure
    pi_pos_sls: Optional[float]
    # Negative internal pressure
    pi_neg_sls: Optional[float]
    # Positive external pressure
    pe_pos_sls: Optional[float]
    # Negative external pressure
    pe_neg_sls: Optional[float]
    # POS value for user display
    pos_sls: Optional[float]
    # NEG value for user display
    neg_sls: Optional[float]

    def __init__(self):
        """
        Constructor for the WindPressure class
        :param pi_pos: The positive internal pressure
        :param pi_neg: The negative internal pressure
        :param pe_pos: The positive external pressure
        :param pe_neg: The negative external pressure
        """
        # Set the attributes
        self.pi_pos_uls = None
        self.pi_neg_uls = None
        self.pe_pos_uls = None
        self.pe_neg_uls = None
        self.pos_uls = None
        self.neg_uls = None
        self.pi_pos_sls = None
        self.pi_neg_sls = None
        self.pe_pos_sls = None
        self.pe_neg_sls = None
        self.pos_sls = None
        self.neg_sls = None

    def __str__(self):
        """
        Returns a string representation of the WindPressure object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"pi_pos_uls: {self.pi_pos_uls}\n"
                f"pi_neg_uls: {self.pi_neg_uls}\n"
                f"pe_pos_uls: {self.pe_pos_uls}\n"
                f"pe_neg_uls: {self.pe_neg_uls}\n"
                f"pos_uls: {self.pos_uls}\n"
                f"neg_uls: {self.neg_uls}\n"
                f"pi_pos_sls: {self.pi_pos_sls}\n"
                f"pi_neg_sls: {self.pi_neg_sls}\n"
                f"pe_pos_sls: {self.pe_pos_sls}\n"
                f"pe_neg_sls: {self.pe_neg_sls}\n"
                f"pos_sls: {self.pos_sls}\n"
                f"neg_sls: {self.neg_sls}")


class WindPressureBuilderInterface:
    """
    Builder interface for the WindPressure class
    """

    def reset(self):
        pass

    def set_pi_pos_uls(self, pi_pos_uls: float):
        pass

    def set_pi_neg_uls(self, pi_neg_uls: float):
        pass

    def set_pe_pos_uls(self, pe_pos_uls: float):
        pass

    def set_pe_neg_uls(self, pe_neg_uls: float):
        pass

    def set_pos_uls(self):
        pass

    def set_neg_uls(self):
        pass

    def set_pi_pos_sls(self, pi_pos_sls: float):
        pass

    def set_pi_neg_sls(self, pi_neg_sls: float):
        pass

    def set_pe_pos_sls(self, pe_pos_sls: float):
        pass

    def set_pe_neg_sls(self, pe_neg_sls: float):
        pass

    def set_pos_sls(self):
        pass

    def set_neg_sls(self):
        pass

    def get_pi_pos_uls(self) -> float:
        pass

    def get_pi_neg_uls(self) -> float:
        pass

    def get_pe_pos_uls(self) -> float:
        pass

    def get_pe_neg_uls(self) -> float:
        pass

    def get_pos_uls(self) -> float:
        pass

    def get_neg_uls(self) -> float:
        pass

    def get_pi_pos_sls(self) -> float:
        pass

    def get_pi_neg_sls(self) -> float:
        pass

    def get_pe_pos_sls(self) -> float:
        pass

    def get_pe_neg_sls(self) -> float:
        pass

    def get_pos_sls(self) -> float:
        pass

    def get_neg_sls(self) -> float:
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

    def set_pi_pos_uls(self, pi_pos_uls: float):
        """
        Sets the positive internal pressure
        :param pi_pos: The positive internal pressure
        :return:
        """
        self.wind_pressure.pi_pos_uls = pi_pos_uls

    def set_pi_neg_uls(self, pi_neg_uls: float):
        """
        Sets the negative internal pressure
        :param pi_neg: The negative internal pressure
        :return:
        """
        self.wind_pressure.pi_neg_uls = pi_neg_uls

    def set_pe_pos_uls(self, pe_pos_uls: float):
        """
        Sets the positive external pressure
        :param pe_pos: The positive external pressure
        :return:
        """
        self.wind_pressure.pe_pos_uls = pe_pos_uls

    def set_pe_neg_uls(self, pe_neg_uls: float):
        """
        Sets the negative external pressure
        :param pe_neg: The negative external pressure
        :return:
        """
        self.wind_pressure.pe_neg_uls = pe_neg_uls

    def set_pos_uls(self):
        assert self.wind_pressure.pe_pos_uls is not None
        assert self.wind_pressure.pi_neg_uls is not None
        self.wind_pressure.pos_uls = self.wind_pressure.pe_pos_uls - self.wind_pressure.pi_neg_uls

    def set_neg(self):
        assert self.wind_pressure.pe_neg_uls is not None
        assert self.wind_pressure.pi_pos_uls is not None
        self.wind_pressure.neg_uls = self.wind_pressure.pe_neg_uls - self.wind_pressure.pi_pos_uls

    def set_pi_pos_sls(self, pi_pos_sls: float):
        """
        Sets the positive internal pressure
        :param pi_pos: The positive internal pressure
        :return:
        """
        self.wind_pressure.pi_pos_sls = pi_pos_sls

    def set_pi_neg_sls(self, pi_neg_sls: float):
        """
        Sets the negative internal pressure
        :param pi_neg: The negative internal pressure
        :return:
        """
        self.wind_pressure.pi_neg_sls = pi_neg_sls

    def set_pe_pos_sls(self, pe_pos_sls: float):
        """
        Sets the positive external pressure
        :param pe_pos: The positive external pressure
        :return:
        """
        self.wind_pressure.pe_pos_sls = pe_pos_sls

    def set_pe_neg_sls(self, pe_neg_sls: float):
        """
        Sets the negative external pressure
        :param pe_neg: The negative external pressure
        :return:
        """
        self.wind_pressure.pe_neg_sls = pe_neg_sls

    def set_pos_sls(self):
        assert self.wind_pressure.pe_pos_sls is not None
        assert self.wind_pressure.pi_neg_sls is not None
        self.wind_pressure.pos_sls = self.wind_pressure.pe_pos_sls - self.wind_pressure.pi_neg_sls

    def set_neg_sls(self):
        assert self.wind_pressure.pe_neg_sls is not None
        assert self.wind_pressure.pi_pos_sls is not None
        self.wind_pressure.neg_sls = self.wind_pressure.pe_neg_sls - self.wind_pressure.pi_pos_sls

    def get_pi_pos_uls(self) -> float:
        """
        Returns the positive internal pressure
        :return: The positive internal pressure
        """
        return self.wind_pressure.pi_pos_uls

    def get_pi_neg_uls(self) -> float:
        """
        Returns the negative internal pressure
        :return: The negative internal pressure
        """
        return self.wind_pressure.pi_neg_uls

    def get_pe_pos_uls(self) -> float:
        """
        Returns the positive external pressure
        :return: The positive external pressure
        """
        return self.wind_pressure.pe_pos_uls

    def get_pe_neg_uls(self) -> float:
        """
        Returns the negative external pressure
        :return: The negative external pressure
        """
        return self.wind_pressure.pe_neg_uls

    def get_pos_uls(self) -> float:
        """
        Returns the positive pressure
        :return: The positive pressure
        """
        return self.wind_pressure.pos_uls

    def get_neg_uls(self) -> float:
        """
        Returns the negative pressure
        :return: The negative pressure
        """
        return self.wind_pressure.neg_uls

    def get_pi_pos_sls(self) -> float:
        """
        Returns the positive internal pressure
        :return: The positive internal pressure
        """
        return self.wind_pressure.pi_pos_sls

    def get_pi_neg_sls(self) -> float:
        """
        Returns the negative internal pressure
        :return: The negative internal pressure
        """
        return self.wind_pressure.pi_neg_sls

    def get_pe_pos_sls(self) -> float:
        """
        Returns the positive external pressure
        :return: The positive external pressure
        """
        return self.wind_pressure.pe_pos_sls

    def get_pe_neg_sls(self) -> float:
        """
        Returns the negative external pressure
        :return: The negative external pressure
        """
        return self.wind_pressure.pe_neg_sls

    def get_pos_sls(self) -> float:
        """
        Returns the positive pressure
        :return: The positive pressure
        """
        return self.wind_pressure.pos_sls

    def get_neg_sls(self) -> float:
        """
        Returns the negative pressure
        :return: The negative pressure
        """
        return self.wind_pressure.neg_sls

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
