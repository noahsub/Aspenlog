########################################################################################################################
# canadian_postal_code_data.py
# This file contains the class for the canadian postal code data
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

########################################################################################################################
# GLOBALS
########################################################################################################################

# Required for SQLAlchemy to use the ORM
BASE = declarative_base()


########################################################################################################################
# CANADIAN POSTAL CODE DATA CLASS
########################################################################################################################

class CanadianPostalCodeData(BASE):
    """
    Class for the climatic data
    """
    # The name of the table
    __tablename__ = 'CanadianPostalCodeData'
    # The ID of the entry
    ID = Column(Integer, primary_key=True)
    # The postal code of the location
    postal_code = Column(String(255))
    # The city of the location
    city = Column(String(255))
    # The province of the location
    province = Column(String(255))
    # The time zone of the location
    time_zone = Column(Integer)
    # The latitude of the location
    latitude = Column(Float)
    # The longitude of the location
    longitude = Column(Float)
