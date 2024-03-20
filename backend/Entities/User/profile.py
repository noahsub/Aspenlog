########################################################################################################################
# profile.py
# This file contains classes that represent the profile of a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# MAIN CLASS
########################################################################################################################


class Profile:
    """
    This class is used to store all the information regarding a user's profile
    """

    # The username of the user
    username: str
    # The first name of the user
    first_name: str
    # The last name of the user
    last_name: str
    # The email of the user
    email: str

    def __init__(self, username: str, first_name: str, last_name: str, email: str):
        """
        Initializes the Profile object
        :param username: The username of the user
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param email: The email of the user
        """
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
