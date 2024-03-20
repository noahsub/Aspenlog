########################################################################################################################
# dimensions.py
# This file contains classes that represent the dimensions of a building.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################


from typing import Optional


########################################################################################################################
# MAIN CLASS
########################################################################################################################


class Dimensions:
    """
    Represents the dimensions of a building
    """

    # height of the building
    height: Optional[float]
    # height of the eave
    height_eave: Optional[float]
    # height of the ridge
    height_ridge: Optional[float]
    # width of the building
    width: Optional[float]

    def __init__(self):
        # Initialize everything to None so that the associated builder class can handle assignments
        self.height = None
        self.height_eave = None
        self.height_ridge = None
        self.width = None

    def __str__(self):
        """
        String representation of the Dimensions class
        :return:
        """
        # Print each attribute and its value on a new line
        return (
            f"height: {self.height}\n"
            f"height_eave: {self.height_eave}\n"
            f"height_ridge: {self.height_ridge}\n"
            f"width: {self.width}"
        )


########################################################################################################################
# BUILDER CLASSES
########################################################################################################################


class DimensionsBuilderInterface:
    """
    Builder interface for the Dimensions class
    """

    def reset(self):
        pass

    def set_height(self, height: float):
        pass

    def set_height_eave(self, height_eave: float):
        pass

    def set_height_ridge(self, height_ridge: float):
        pass

    def set_width(self, width: float):
        pass

    def get_height(self):
        pass

    def get_height_eave(self):
        pass

    def get_height_ridge(self):
        pass

    def get_width(self):
        pass


class BasicDimensionsBuilder(DimensionsBuilderInterface):
    dimensions: Dimensions

    def __init__(self):
        """
        Constructor for the BasicDimensionsBuilder class
        """
        # Initialize the builder to its initial state
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.dimensions = Dimensions()

    def set_height(self, height: float):
        """
        Sets the height attribute of the Dimensions class
        :param height: The height of the building
        :return: None
        """
        self.dimensions.height = height

    def set_width(self, width: float):
        """
        Sets the width attribute of the Dimensions class
        :param width: The width of the building
        :return: None
        """
        self.dimensions.width = width

    def get_height(self):
        """
        Returns the height attribute of the Dimensions class
        :return: The height of the building
        """
        return self.dimensions.height

    def get_width(self):
        """
        Returns the width attribute of the Dimensions class
        :return: The width of the building
        """
        return self.dimensions.width

    def get_dimensions(self):
        """
        Returns the dimensions object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed dimensions object.
        """
        dimensions = self.dimensions
        self.reset()
        return dimensions


class EaveRidgeDimensionsBuilder(DimensionsBuilderInterface):
    dimensions: Dimensions

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        # Initialize the builder to its initial state
        self.dimensions = Dimensions()

    def set_height_eave(self, height_eave: float):
        """
        Sets the height_eave attribute of the Dimensions class
        :param height_eave: The height of the eave of the building
        :return: None
        """
        self.dimensions.height_eave = height_eave

    def set_height_ridge(self, height_ridge: float):
        """
        The height_ridge attribute of the Dimensions class
        :param height_ridge: The height of the ridge of the building
        :return: None
        """
        self.dimensions.height_ridge = height_ridge

    def set_width(self, width: float):
        """
        The width attribute of the Dimensions class
        :param width: The width of the building
        :return: None
        """
        self.dimensions.width = width

    def compute_height(self):
        """
        The height attribute of the Dimensions class
        :return: None
        """
        assert self.dimensions.height_eave is not None
        assert self.dimensions.height_ridge is not None
        # Compute the average of the eave and ridge heights
        self.dimensions.height = (
            self.dimensions.height_eave + self.dimensions.height_ridge
        ) / 2

    def get_height_eave(self):
        """
        Returns the height_eave attribute of the Dimensions class
        :return: The height of the eave of the building
        """
        return self.dimensions.height_eave

    def get_height_ridge(self):
        """
        Returns the height_ridge attribute of the Dimensions class
        :return: The height of the ridge of the building
        """
        return self.dimensions.height_ridge

    def get_width(self):
        """
        Returns the width attribute of the Dimensions class
        :return: The width of the building
        """
        return self.dimensions.width

    def get_dimensions(self):
        """
        Returns the dimensions object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed dimensions object.
        """
        dimensions = self.dimensions
        self.reset()
        return dimensions


class DimensionsDirector:
    @staticmethod
    def construct_basic_dimensions(builder: DimensionsBuilderInterface):
        raise NotImplementedError

    @staticmethod
    def construct_eave_ridge_dimensions(builder: DimensionsBuilderInterface):
        raise NotImplementedError
