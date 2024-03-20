########################################################################################################################
# roof_manager.py
# This file manages the creation of a roof object for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Entities.Building.roof import RoofBuilder


########################################################################################################################
# MANAGER
########################################################################################################################


def process_roof_data(
    w_roof: float, l_roof: float, slope: float, uniform_dead_load: float
):
    """
    Processes the roof data and creates a roof object
    :param w_roof: The width of the roof
    :param l_roof: The length of the roof
    :param slope: The slope of the roof
    :param uniform_dead_load: The uniform dead load of the roof
    :return: A roof object
    """
    # Create a roof builder object
    roof_builder = RoofBuilder()
    # Set the roof data
    roof_builder.set_w_roof(w_roof)
    roof_builder.set_l_roof(l_roof)
    roof_builder.set_slope(slope)
    roof_builder.compute_wall_slope()
    roof_builder.set_wp(uniform_dead_load)
    # Return the roof object
    return roof_builder.get_roof()
