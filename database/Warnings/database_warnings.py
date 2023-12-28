########################################################################################################################
# database_warnings.py
# This file contains the warnings for the database
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################
import warnings


########################################################################################################################
# WARNING CLASSES
########################################################################################################################
class AlreadyExistsWarning(Warning):
    """
    Warning for when an item already exists in the database
    """
    pass


def already_exists_warning(item: str, database_name: str):
    """
    Function that raises a warning for when an item already exists in the database
    :param item: The item in question
    :param database_name: The name of the database
    :return: None
    """
    # Warn the user that the item already exists in the database
    warnings.warn(f"{item} already exists in {database_name}", category=AlreadyExistsWarning)
