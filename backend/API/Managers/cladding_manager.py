########################################################################################################################
# cladding_manager.py
# This file manages the creation of a cladding object for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Entities.Building.cladding import CladdingBuilder


########################################################################################################################
# MANAGER
########################################################################################################################

def process_cladding_data(c_top: float, c_bot: float):
    """
    Processes the cladding data and creates a cladding object
    :param c_top: The top cladding
    :param c_bot: The bottom cladding
    :return: A cladding object
    """
    # Create a cladding builder object
    cladding_builder = CladdingBuilder()
    # Set the cladding data
    cladding_builder.set_c_top(c_top)
    cladding_builder.set_c_bot(c_bot)
    # Return the cladding object
    return cladding_builder.get_cladding()
