########################################################################################################################
# dimensions_manager.py
# This file manages the creation of a dimensions object for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Entities.Building.dimensions import BasicDimensionsBuilder, EaveRidgeDimensionsBuilder


########################################################################################################################
# MANAGER
########################################################################################################################

def process_dimension_data(width: float, height: float = None, eave_height: float = None, ridge_height: float = None):
    """
    Processes the dimension data and creates a dimensions object
    :param width: The width of the building
    :param height: The height of the building
    :param eave_height: The eave height of the building
    :param ridge_height: The ridge height of the building
    :return: A dimensions object
    """
    # If the eave height and ridge height are not provided, use the basic dimensions builder
    if eave_height is None and ridge_height is None:
        dimensions_builder = BasicDimensionsBuilder()
        dimensions_builder.set_height(height)
        dimensions_builder.set_width(width)
    # If the eave height and ridge height are provided, use the eave ridge dimensions builder
    else:
        dimensions_builder = EaveRidgeDimensionsBuilder()
        dimensions_builder.set_width(width)
        dimensions_builder.set_height_eave(eave_height)
        dimensions_builder.set_height_ridge(ridge_height)
        dimensions_builder.compute_height()
    # Return the dimensions object
    return dimensions_builder.get_dimensions()
