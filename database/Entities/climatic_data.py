########################################################################################################################
# climatic_data.py
# This file contains the class for the climatic data
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
# ClIMATIC DATA CLASS
########################################################################################################################


class ClimaticData(BASE):
    """
    Class for the climatic data
    """

    # The name of the table
    __tablename__ = "ClimaticData"
    # The ID of the entry
    ID = Column(Integer, primary_key=True)
    # The name of the location
    ProvinceAndLocation = Column(String(255))
    # The latitude of the location
    Latitude = Column(Float)
    # The longitude of the location
    Longitude = Column(Float)
    # The elevation of the location
    Elev_m = Column(Integer)
    # Climatic columns
    Jan_2_5_percent_C = Column(Float)
    Jan_1_percent_C = Column(Float)
    July_Dry_C = Column(Float)
    July_Wet_C = Column(Float)
    DegreeDaysBelow18C = Column(Integer)
    Rain_15_Min_mm = Column(Integer)
    OneDayRain_1_50_mm = Column(Integer)
    Ann_Rain_mm = Column(Integer)
    MoistIndex = Column(Float)
    Ann_Tot_Ppn_mm = Column(Integer)
    DrivingRainWindPressures_Pa_1_5 = Column(Integer)
    SnowLoad_kPa_1_50_Ss = Column(Float)
    SnowLoad_kPa_1_50_Sr = Column(Float)
    HourlyWindPressures_kPa_1_10 = Column(Float)
    HourlyWindPressures_kPa_1_50 = Column(Float)
