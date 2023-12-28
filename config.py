########################################################################################################################
# config.py
# This file contains the configuration functions for the project
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import os

########################################################################################################################
# GLOBALS
########################################################################################################################

# The project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


########################################################################################################################
# CONFIG FUNCTIONS
########################################################################################################################

def get_file_path(relative_path):
    """
    Gets the absolute file path from the relative path
    :param relative_path: The relative path from the source root
    :return: The absolute file path combined with the relative path
    """
    # Return the absolute file path combined with the relative path
    return os.path.join(PROJECT_DIR, relative_path)
