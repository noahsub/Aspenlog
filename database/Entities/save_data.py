########################################################################################################################
# IMPORTS
########################################################################################################################

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base

########################################################################################################################
# GLOBALS
########################################################################################################################

# Required for SQLAlchemy to use the ORM
BASE = declarative_base()


########################################################################################################################
# CANADIAN POSTAL CODE DATA CLASS
########################################################################################################################

class SaveData(BASE):
    """
    Class for the climatic data
    """
    # The name of the table
    __tablename__ = 'SaveData'
    # table contains id, date modified, and json data columns
    ID = Column(Integer, primary_key=True)
    Username = Column(String)
    DateModified = Column(DateTime)
    JsonData = Column(String)
