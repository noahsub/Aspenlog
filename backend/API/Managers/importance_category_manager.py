########################################################################################################################
# importance_category_manager.py
# This file manages the processing of importance category data.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.importance_factor_constants import ImportanceFactor


########################################################################################################################
# MANAGER
########################################################################################################################


def process_importance_category_data(importance_category: str):
    """
    Processes the importance category data and returns the importance factor
    :param importance_category: The importance category as a string
    :return: The importance factor enum
    """
    match importance_category:
        case "LOW":
            return ImportanceFactor.LOW
        case "NORMAL":
            return ImportanceFactor.NORMAL
        case "HIGH":
            return ImportanceFactor.HIGH
        case "POST_DISASTER":
            return ImportanceFactor.POST_DISASTER
