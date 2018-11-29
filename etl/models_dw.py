from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DIM_city(Base):
    __tablename__ = 'DIM_city'
    __table_args__ = {'schema': 'tcc'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    created_at = Column('created_at', DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_city')


class DIM_district(Base):
    __tablename__ = 'DIM_district'
    __table_args__ = {'schema': 'tcc'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    created_at = Column('created_at', DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_district')


class DIM_neighborhood(Base):
    __tablename__ = 'DIM_neighborhood'
    __table_args__ = {'schema': 'tcc'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    created_at = Column('created_at', DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_neighborhood')


class DIM_time(Base):
    __tablename__ = 'DIM_time'
    __table_args__ = {'schema': 'tcc'}

    time_key = Column('time_key', Integer, primary_key=True)
    date_occur = Column('date_occur', Date, default=datetime.utcnow())
    month = Column('month', Integer)
    year = Column('year', Integer)
    quarter = Column('quarter', Integer)
    semester = Column('semester', Integer)
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_time')


class FACT_thefts(Base):
    __tablename__ = 'FACT_thefts'
    __table_args__ = {'schema': 'tcc'}

    id = Column('id', Integer, primary_key=True)
    DIM_time_id = Column('DIM_time_id', Integer, ForeignKey("tcc.DIM_time.time_key"))
    DIM_neighborhood_id = Column('DIM_neighborhood_id', Integer, ForeignKey("tcc.DIM_neighborhood.id"), default=None,
                                 nullable=True)
    DIM_district_id = Column('DIM_district_id', Integer, ForeignKey("tcc.DIM_district.id"), default=None, nullable=True)
    DIM_city_id = Column('DIM_city_id', Integer, ForeignKey("tcc.DIM_city.id"), default=None, nullable=True)
    theft = Column('theft', Integer)

    dim_time = relationship("DIM_time", back_populates='FACT_thefts')
    dim_neighborhood = relationship("DIM_neighborhood", back_populates='FACT_thefts')
    dim_district = relationship("DIM_district", back_populates='FACT_thefts')
    dim_city = relationship("DIM_city", back_populates='FACT_thefts')
