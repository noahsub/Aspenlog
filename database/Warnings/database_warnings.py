########################################################################################################################
# database_warnings.py
# This file contains the warnings for the database
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
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


class UsernameTakenWarning(Warning):
    """
    Warning for when a username is already taken in the database
    """

    pass


class UsernameNotValidWarning(Warning):
    """
    Warning for when a username is not considered valid
    """

    pass


class EmailTakenWarning(Warning):
    """
    Warning for when an email is already taken in the database
    """

    pass


class NotValidPasswordWarning(Warning):
    """
    Warning for when a password is not considered valid
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
    warnings.warn(
        f"{item} already exists in {database_name}", category=AlreadyExistsWarning
    )


def username_taken_warning(username: str):
    """
    Function that raises a warning for when a username is already taken in the database
    :param username: The username that is already taken
    :param database_name: The name of the database
    :return: None
    """
    # Warn the user that the username is already taken in the database
    warnings.warn(
        f"Username '{username}' is already taken", category=UsernameTakenWarning
    )


def username_not_valid_warning(username: str):
    """
    Function that raises a warning for when a username is not considered valid
    :param username: The username that is not considered valid
    :return: None
    """
    warning_message = (
        f"Username '{username}' is not considered valid. Please ensure the following:\n"
        f" - Minimum length of 5 characters\n"
        f" - Maximum length of 20 characters\n"
        f" - Only alphanumeric characters\n"
        f" - Avoid common words and patterns"
    )

    warnings.warn(warning_message, category=UsernameNotValidWarning)


def email_taken_warning(email: str):
    """
    Function that raises a warning for when an email is already taken in the database
    :param email: The email that is already taken
    :param database_name: The name of the database
    :return: None
    """
    # Warn the user that the email is already taken in the database
    warnings.warn(f"Email '{email}' is already taken", category=EmailTakenWarning)


def not_valid_password_warning(password: str):
    """
    Function that raises a warning for when a password is not considered valid
    :param password: The password that is not considered valid
    :return: None
    """
    warning_message = (
        f"Password '{password}' is not considered valid. Please ensure the following:\n"
        f" - Minimum length of 10 characters\n"
        f" - At least one uppercase letter\n"
        f" - At least one lowercase letter\n"
        f" - At least one digit\n"
        f" - At least one special character (!@#$%^&*()-_=+[]{{}}|;:'\",.<>/?`~)\n"
        f" - Avoid common words and patterns"
    )

    warnings.warn(warning_message, category=NotValidPasswordWarning)
