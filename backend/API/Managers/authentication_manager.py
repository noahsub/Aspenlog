########################################################################################################################
# authentication_manager.py
# This file manages the authentication of users.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import os
from datetime import datetime

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker

from backend.API.Managers.user_data_manager import set_user_profile, check_user_exists
from backend.Entities.User.profile import Profile
from config import get_file_path
from database.Constants.connection_constants import PrivilegeType
from database.Entities.authentication_data import AuthenticationData
from database.Entities.database_connection import DatabaseConnection
from database.Population import populate_authentication_data
from database.Warnings.database_warnings import (
    not_valid_password_warning,
    email_taken_warning,
    username_taken_warning,
    username_not_valid_warning,
)

########################################################################################################################
# GLOBALS AND CONSTANTS
########################################################################################################################

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key to sign and verify JWT tokens
# Get secret key from environment variable from data/EnvironmentVariables/.env
load_dotenv(dotenv_path=get_file_path(relative_path="data/EnvironmentVariables/.env"))
SECRET_KEY = os.getenv("API_SECRET_KEY")
ALGORITHM = "HS256"

########################################################################################################################
# MANAGER
########################################################################################################################


def hash_password(password: str) -> tuple[bytes, bytes]:
    """
    Hashes a password using bcrypt
    :param password: The password to hash
    :return: The hashed password and the salt used to hash the password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode("utf-8"), salt=salt), salt


def valid_username(username: str) -> bool:
    """
    Checks if a username is valid
    :param username: The username to check
    :return: A boolean indicating if the username is valid
    """
    # connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # Check if the username exists
    username_exists = (
        controller.query(AuthenticationData).filter_by(username=username).first()
        is not None
    )

    # Check if the username is alphanumeric and between 5 and 20 characters long
    username_valid = (
        5 <= len(username) <= 20 and username.isalnum() and username.isalnum()
    )

    # Close the connection to the database
    new_connection.close()

    # If the username exists, then the username is not valid
    if username_exists:
        username_taken_warning(username)
        return False

    # If the username is not alphanumeric and between 5 and 20 characters long, then the username is not valid
    if not username_valid:
        username_not_valid_warning(username)
        return False

    # Otherwise, the username is valid
    return True


def valid_email(email: str) -> bool:
    """
    Checks if an email is valid
    :param email: The email to check
    :return: A boolean indicating if the email is valid
    """
    # Connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # Check if the email exists
    email_exists = (
        controller.query(AuthenticationData).filter_by(email=email).first() is not None
    )

    # Close the connection to the database
    new_connection.close()

    # If the email exists, then the email is not valid
    if email_exists:
        email_taken_warning(email)
        return False

    # Otherwise, the email is valid
    return True


def valid_password(password: str) -> bool:
    """
    Checks if a password is valid
    :param password: The password to check
    :return: A boolean indicating if the password is valid
    """
    # Check if the password is at least 10 characters long
    if len(password) < 10:
        not_valid_password_warning(password)
        return False

    # Check if the password has at least one uppercase letter
    if not any(char.isupper() for char in password):
        not_valid_password_warning(password)
        return False

    # Check if the password has at least one lowercase letter
    if not any(char.islower() for char in password):
        not_valid_password_warning(password)
        return False

    # Check if the password has at least one digit
    if not any(char.isdigit() for char in password):
        not_valid_password_warning(password)
        return False

    # Check if the password has at least one special character
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in password):
        not_valid_password_warning(password)
        return False

    return True


def signup(username: str, first_name: str, last_name: str, password: str, email: str):
    """
    Signs up a user
    :param username: The username of the user
    :param first_name: The first name of the user
    :param last_name: The last name of the user
    :param password: The password of the user
    :param email: The email of the user
    :return: A boolean indicating if the user was signed up
    """
    # Check if the username, email, and password are valid
    if not all(
        [valid_username(username), valid_email(email), valid_password(password)]
    ):
        # Return False to indicate that the user was not signed up
        return False

    # Hash the password
    hashed_password, salt = hash_password(password)

    # Add the user to the database
    authentication_data = AuthenticationData(
        username=username,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hashed_password,
        salt=salt,
        email=email,
        signup_date=datetime.now(),
    )
    populate_authentication_data.add_entry(authentication_data)

    # Return True to indicate that the user was signed up
    return True


def login(username: str, password: str):
    """
    Logs in a user
    :param username: The username of the user
    :param password: The password of the user
    :return: The API token for the user if the user was logged in, otherwise False
    """
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # Get the user's details from the database
    authentication_data = (
        controller.query(AuthenticationData).filter_by(username=username).first()
    )

    # If the user does not exist, return False
    if authentication_data is None:
        return False

    # Set the user's profile
    profile = Profile(
        username=authentication_data.username,
        first_name=authentication_data.first_name,
        last_name=authentication_data.last_name,
        email=authentication_data.email,
    )
    check_user_exists(username)
    set_user_profile(username, profile)

    # Close the connection to the database
    new_connection.close()

    # Hash the password
    hashed_password = bcrypt.hashpw(
        password=password.encode("utf-8"), salt=authentication_data.salt
    )

    # If the hashed password matches the hashed password in the database, return the API token for the user
    if hashed_password == authentication_data.hashed_password:
        token_data = {"sub": username}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"token_type": "bearer", "access_token": token}

    # Otherwise, return False
    return False


def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decodes a token
    :param token: The API token to decode
    :return: The username of the user if the token is valid, otherwise raise an HTTPException
    """
    # The exception to raise if the token is not valid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # If the username is None, raise an HTTPException
        if username is None:
            raise credentials_exception
        # Return the username
        return username
    # If the token is not valid, raise an HTTPException
    except JWTError:
        raise credentials_exception
