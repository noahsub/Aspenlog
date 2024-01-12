from typing import Optional

from backend.Entities.Seismic.seismic_factor import SeismicFactor


class SeismicLoad:
    """
    This class is used to store all the information regarding seismic loads
    """
    # The seismic factor
    factor: Optional[SeismicFactor]
    # Height factor
    ax: Optional[float]
    # Horizontal force factor for the part or portion of the building
    sp: Optional[float]
    # Specified lateral earthquake force
    vp: Optional[float]
    vp_snow: Optional[float]

    def __init__(self):
        # Assign the attributes
        self.factor = None
        self.ax = None
        self.sp = None
        self.vp = None
        self.vp_snow = None

    def __str__(self):
        """
        Returns a string representation of the SeismicLoad object
        :return:
        """
        # Special formatting for subclasses
        factor_str = '\n  ' + '\n  '.join(str(self.factor).split('\n'))
        # Print each attribute and its value on a new line
        return (f"factor: {factor_str}\n"
                f"ax: {self.ax}\n"
                f"sp: {self.sp}\n"
                f"vp: {self.vp}\n"
                f"vp_snow: {self.vp_snow}")


class SeismicLoadBuilderInterface:
    """
    Builder interface for the SeismicLoad class
    """

    def reset(self) -> None:
        pass

    def set_factor(self, factor: SeismicFactor) -> None:
        pass

    def set_ax(self, ax: float) -> None:
        pass

    def set_sp(self, sp: float) -> None:
        pass

    def set_vp(self, vp: float) -> None:
        pass

    def set_vp_snow(self, vp_snow: float) -> None:
        pass

    def get_factor(self) -> SeismicFactor:
        pass

    def get_ax(self) -> float:
        pass

    def get_sp(self) -> float:
        pass

    def get_vp(self) -> float:
        pass

    def get_vp_snow(self) -> float:
        pass


class SeismicLoadBuilder(SeismicLoadBuilderInterface):
    """
    Concrete builder class for the SeismicLoad class
    """
    seismic_load: SeismicLoad

    def __init__(self):
        self.reset()

    def reset(self):
        self.seismic_load = SeismicLoad()

    def set_factor(self, factor: SeismicFactor):
        self.seismic_load.factor = factor

    def set_ax(self, ax: float):
        self.seismic_load.ax = ax

    def set_sp(self, sp: float):
        self.seismic_load.sp = sp

    def set_vp(self, vp: float):
        self.seismic_load.vp = vp

    def set_vp_snow(self, vp_snow: float):
        self.seismic_load.vp_snow = vp_snow

    def get_factor(self) -> SeismicFactor:
        return self.seismic_load.factor

    def get_ax(self) -> float:
        return self.seismic_load.ax

    def get_sp(self) -> float:
        return self.seismic_load.sp

    def get_vp(self) -> float:
        return self.seismic_load.vp

    def get_vp_snow(self) -> float:
        return self.seismic_load.vp_snow

    def get_seismic_load(self):
        seismic_load = self.seismic_load
        self.reset()
        return seismic_load


class SeismicLoadDirector:
    @staticmethod
    def construct_seismic_load(builder: SeismicLoadBuilderInterface):
        raise NotImplementedError
