########################################################################################################################
# login_input.py
# This file contains the input model for the login object.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from pydantic import BaseModel


########################################################################################################################
# MODEL
########################################################################################################################


class LoginInput(BaseModel):
    """
    The input model for the login object
    """

    # The username of the user
    username: str
    # The password of the user
    password: str
