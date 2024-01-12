from typing import Optional


class SeismicFactor:
    """
    This class is used to store the seismic factor information
    """
    # Element or component force amplification factor
    ar: Optional[float]
    # Element of component response modification factor
    rp: Optional[float]
    # Element of component factor
    cp: Optional[float]

    def __init__(self):
        # Set the attributes
        self.ar = None
        self.rp = None
        self.cp = None

    def __str__(self):
        """
        Returns a string representation of the SeismicFactor object
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"ar: {self.ar}\n"
                f"rp: {self.rp}\n"
                f"cp: {self.cp}")


class SeismicFactorBuilderInterface:
    """
    Builder interface for the SeismicFactor class
    """

    def reset(self) -> None:
        pass

    def set_ar(self, ar: float) -> None:
        pass

    def set_rp(self, rp: float) -> None:
        pass

    def set_cp(self, cp: float) -> None:
        pass

    def get_ar(self) -> float:
        pass

    def get_rp(self) -> float:
        pass

    def get_cp(self) -> float:
        pass


class SeismicFactorBuilder(SeismicFactorBuilderInterface):
    """
    Concrete builder class for the SeismicFactor class
    """
    seismic_factor: SeismicFactor

    def __init__(self):
        self.reset()

    def reset(self):
        self.seismic_factor = SeismicFactor()

    def set_ar(self, ar: float = 1):
        self.seismic_factor.ar = ar

    def set_rp(self, rp: float = 2.5):
        self.seismic_factor.rp = rp

    def set_cp(self, cp: float = 1):
        self.seismic_factor.cp = cp

    def get_ar(self) -> float:
        return self.seismic_factor.ar

    def get_rp(self) -> float:
        return self.seismic_factor.rp

    def get_cp(self) -> float:
        return self.seismic_factor.cp

    def get_seismic_factor(self) -> SeismicFactor:
        seismic_factor = self.seismic_factor
        self.reset()
        return seismic_factor


class SeismicFactorDirector:
    @staticmethod
    def construct_seismic_factor(builder: SeismicFactorBuilderInterface):
        raise NotImplementedError
