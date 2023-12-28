########################################################################################################################
# wind_speed_data.py
# This file contains the class for the wind speed data
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
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
