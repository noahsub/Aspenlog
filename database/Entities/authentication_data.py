########################################################################################################################
# authentication_data.py
# This file contains the class for the authentication data entries in the database
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from sqlalchemy import Column, String, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base

########################################################################################################################
# GLOBALS
########################################################################################################################

# Required for SQLAlchemy to use the ORM
BASE = declarative_base()


########################################################################################################################
# CANADIAN POSTAL CODE DATA CLASS
########################################################################################################################


class AuthenticationData(BASE):
    """
    Class for the climatic data
    """

    # The name of the table
    __tablename__ = "AuthenticationData"
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(LargeBinary)
    salt = Column(LargeBinary)
    email = Column(String, unique=True)
    signup_date = Column(DateTime)
