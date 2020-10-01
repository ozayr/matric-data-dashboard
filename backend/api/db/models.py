from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.types import Date
from .database import Base


class DataBaseRecord(Base):
    __tablename__ = "Records"

    emis = Column(Integer, primary_key=True, index=True)
    centre_no = Column(Integer)
    name = Column(String(255))

    wrote_2014 = Column(Integer)
    passed_2014 = Column(Integer)
    wrote_2015 = Column(Integer)
    passed_2015 = Column(Integer)
    wrote_2016 = Column(Integer)
    passed_2016 = Column(Integer)

    province = Column(String)

    pass_rate_2014 = Column(Float)
    pass_rate_2015 = Column(Float)
    pass_rate_2016 = Column(Float)
