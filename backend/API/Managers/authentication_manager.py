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
from database.Warnings.database_warnings import not_valid_password_warning, email_taken_warning, username_taken_warning, \
    username_not_valid_warning

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key to sign and verify JWT tokens
# Get secret key from environment variable from data/EnvironmentVariables/.env
load_dotenv(dotenv_path=get_file_path(relative_path="data/EnvironmentVariables/.env"))
SECRET_KEY = os.getenv('API_SECRET_KEY')
ALGORITHM = "HS256"


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
        return False

    hashed_password, salt = hash_password(password)
    authentication_data = AuthenticationData(username=username, first_name=first_name, last_name=last_name,
                                             hashed_password=hashed_password, salt=salt, email=email,
                                             signup_date=datetime.now())
    populate_authentication_data.add_entry(authentication_data)

    return True


def login(username: str, password: str):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    authentication_data = controller.query(AuthenticationData).filter_by(username=username).first()

    if authentication_data is None:
        return False

    profile = Profile(username=authentication_data.username, first_name=authentication_data.first_name,
                      last_name=authentication_data.last_name, email=authentication_data.email)
    check_user_exists(username)
    set_user_profile(username, profile)
    new_connection.close()

    hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=authentication_data.salt)

    if hashed_password == authentication_data.hashed_password:
        token_data = {"sub": username}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"token_type": "bearer", "access_token": token}

    return False


def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
