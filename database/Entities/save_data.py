########################################################################################################################
# safe_data.py
# This file contains the class for the save data entries in the database
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

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
    __tablename__ = "SaveData"
    # table contains id, date modified, and json data columns
    ID = Column(Integer, primary_key=True)
    Username = Column(String)
    DateModified = Column(DateTime)
    JsonData = Column(String)
