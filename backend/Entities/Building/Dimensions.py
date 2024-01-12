from typing import Optional


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
        return (f"height: {self.height}\n"
                f"height_eave: {self.height_eave}\n"
                f"height_ridge: {self.height_ridge}\n"
                f"width: {self.width}")


class DimensionsBuilder:
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


class BasicDimensionsBuilder(DimensionsBuilder):
    dimensions: Dimensions

    def __init__(self):
        self.reset()

    def reset(self):
        self.dimensions = Dimensions()

    def set_height(self, height: float):
        self.dimensions.height = height

    def set_width(self, width: float):
        self.dimensions.width = width

    def get_height(self):
        return self.dimensions.height

    def get_width(self):
        return self.dimensions.width

    def get_dimensions(self):
        """
        Returns the dimensions object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed dimensions object.
        """
        dimensions = self.dimensions
        self.reset()
        return dimensions


class EaveRidgeDimensionsBuilder(DimensionsBuilder):
    dimensions: Dimensions

    def __init__(self):
        self.reset()

    def reset(self):
        self.dimensions = Dimensions()

    def set_height_eave(self, height_eave: float):
        self.dimensions.height_eave = height_eave

    def set_height_ridge(self, height_ridge: float):
        self.dimensions.height_ridge = height_ridge

    def set_width(self, width: float):
        self.dimensions.width = width

    def get_height_eave(self):
        return self.dimensions.height_eave

    def get_height_ridge(self):
        return self.dimensions.height_ridge

    def get_width(self):
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
    def construct_basic_dimensions(builder: DimensionsBuilder):
        """
        The width and the height of the building should have already been set within the client code, hence this
        function only checks that the height and width have been set and that the eave and ridge heights have not been.
        :param builder: The builder object to be used to construct the dimensions
        :return:
        """
        assert builder.get_height() is not None
        assert builder.get_width() is not None
        assert builder.get_height_eave() is None
        assert builder.get_height_ridge() is None
        pass

    @staticmethod
    def construct_eave_ridge_dimensions(self, builder: DimensionsBuilder):
        """
        The width and the eave and ridge heights of the building should have already been set within the client code,
        this function, computes the height of the building using the eave and ridge heights.
        :param self:
        :param builder:
        :return:
        """
        # Checks thats everything has been set except for the height of the building.
        assert builder.get_height() is None
        assert builder.get_width() is not None
        assert builder.get_height_eave() is not None
        assert builder.get_height_ridge() is not None

        # Compute the height of the building using the eave and ridge heights.
        builder.set_height((builder.get_height_eave() + builder.get_height_ridge()) / 2)

