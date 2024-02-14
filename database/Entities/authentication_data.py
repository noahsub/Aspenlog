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
    __tablename__ = 'AuthenticationData'
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(LargeBinary)
    salt = Column(LargeBinary)
    email = Column(String, unique=True)
    signup_date = Column(DateTime)
