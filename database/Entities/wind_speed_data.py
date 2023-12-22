from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class WindSpeedData(BASE):
    __tablename__ = 'WindSpeedData'
    ID = Column(Integer, primary_key=True)
    q_KPa = Column(Float)
    V_ms = Column(Float)
