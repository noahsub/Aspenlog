from datetime import datetime
from typing import List

import bcrypt
from sqlalchemy.orm import sessionmaker
from database.Constants.connection_constants import PrivilegeType
from database.Entities.authentication_data import AuthenticationData
from database.Entities.database_connection import DatabaseConnection
from database.Population import populate_authentication_data
from database.Warnings.database_warnings import not_valid_password_warning, email_taken_warning, username_taken_warning, \
    username_not_valid_warning


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt), salt


def valid_username(username: str) -> bool:
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    username_exists = controller.query(AuthenticationData).filter_by(username=username).first() is not None

    username_valid = 5 <= len(username) <= 20 and username.isalnum() and username.isalnum()

    new_connection.close()

    if username_exists:
        username_taken_warning(username)
        return False

    if not username_valid:
        username_not_valid_warning(username)
        return False

    return True


def valid_email(email: str) -> bool:
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    email_exists = controller.query(AuthenticationData).filter_by(email=email).first() is not None
    new_connection.close()

    if email_exists:
        email_taken_warning(email)
        return False

    return True


def valid_password(password: str) -> bool:
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
    if not all([valid_username(username), valid_email(email), valid_password(password)]):
        return

    hashed_password, salt = hash_password(password)
    authentication_data = AuthenticationData(username=username, first_name=first_name, last_name=last_name,
                                             hashed_password=hashed_password, salt=salt, email=email,
                                             signup_date=datetime.now())
    populate_authentication_data.add_entry(authentication_data)


def login(username: str, password: str):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    authentication_data = controller.query(AuthenticationData).filter_by(username=username).first()
    new_connection.close()

    if authentication_data is None:
        return False

    hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=authentication_data.salt)

    if hashed_password == authentication_data.hashed_password:
        return True

    return False



