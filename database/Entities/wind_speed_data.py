########################################################################################################################
# wind_speed_data.py
# This file contains the class for the wind speed data
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

########################################################################################################################
# GLOBALS
########################################################################################################################

# Required for SQLAlchemy to use the ORM
BASE = declarative_base()


########################################################################################################################
# WIND SPEED DATA CLASS
########################################################################################################################

class WindSpeedData(BASE):
    # The name of the table
    __tablename__ = 'WindSpeedData'
    # The ID of the entry
    ID = Column(Integer, primary_key=True)
    # Wind speed columns
    q_KPa = Column(Float)
    V_ms = Column(Float)
