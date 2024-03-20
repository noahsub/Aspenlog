########################################################################################################################
# register_input.py
# This file contains the input model for the register endpoint.
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

class RegisterInput(BaseModel):
    """
    The input model for the register endpoint
    """
    # The username of the user
    username: str
    # The first name of the user
    first_name: str
    # The last name of the user
    last_name: str
    # The password of the user
    password: str
    # The email of the user
    email: str
