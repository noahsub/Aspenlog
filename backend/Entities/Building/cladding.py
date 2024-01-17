from typing import Optional


class Cladding:
    """
    Represents the cladding of a building
    """
    # Height of the tallest part of the cladding components (i.e. where it ends)
    c_top: Optional[float]
    # Height of the lowest part of the cladding components (i.e. where it starts)
    c_bot: Optional[float]

    def __init__(self):
        self.c_top = None
        self.c_bot = None

    def __str__(self):
        """
        String representation of the Cladding class
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"c_top: {self.c_top}\n"
                f"c_bot: {self.c_bot}")


class CladdingBuilderInterface:
    """
    Builder interface for the Cladding class
    """

    def reset(self):
        pass

    def set_c_top(self, c_top: float):
        pass

    def set_c_bot(self, c_bot: float):
        pass

    def get_c_top(self):
        pass

    def get_c_bot(self):
        pass


class CladdingBuilder(CladdingBuilderInterface):
    """
    Concrete builder class for the Cladding class
    """
    cladding: Cladding

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets the builder to its initial state
        :return: None
        """
        self.cladding = Cladding()

    def set_c_top(self, c_top: float):
        """
        Sets the c_top attribute of the Cladding class
        :param c_top: Height of the tallest part of the cladding components (i.e. where it ends)
        :return: None
        """
        self.cladding.c_top = c_top

    def set_c_bot(self, c_bot: float):
        """
        Sets the c_bot attribute of the Cladding class
        :param c_bot: Height of the lowest part of the cladding components (i.e. where it starts)
        :return: None
        """
        self.cladding.c_bot = c_bot

    def get_c_top(self):
        """
        Returns the c_top attribute of the Cladding class
        :return: Height of the tallest part of the cladding components (i.e. where it ends)
        """
        return self.cladding.c_top

    def get_c_bot(self):
        """
        Returns the c_bot attribute of the Cladding class
        :return: Height of the lowest part of the cladding components (i.e. where it starts)
        """
        return self.cladding.c_bot

    def get_cladding(self):
        """
        Returns the cladding object and resets the builder object to its initial state so that it can be used again.
        :return: The constructed cladding object.
        """
        cladding = self.cladding
        self.reset()
        return cladding


class CladdingDirector:
    @staticmethod
    def construct_cladding(builder: CladdingBuilderInterface):
        raise NotImplementedError
