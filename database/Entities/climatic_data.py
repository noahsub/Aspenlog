from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class ClimaticData(BASE):
    __tablename__ = 'ClimaticData'
    ID = Column(Integer, primary_key=True)
    ProvinceAndLocation = Column(String(255))
    Latitude = Column(Float)
    Longitude = Column(Float)
    Elev_m = Column(Integer)
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
