from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    geo_location = Column('geo_location', JSON)
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    city_quantities = relationship("CityQuantity", back_populates='city')


class CityQuantity(Base):
    __tablename__ = 'city_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    theft = Column('theft', Integer)
    date_occurrence = Column('date_occurrence', DateTime)
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    city = relationship("City", back_populates='city_quantities')
    city_id = Column('city_id', Integer, ForeignKey("ssp_go.city.id"))


class Neighborhood(Base):
    __tablename__ = 'neighborhood'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    geo_location = Column('geo_location', JSON)
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    neighborhood_quantity = relationship("NeighborhoodQuantity", back_populates='neighborhood')


class NeighborhoodQuantity(Base):
    __tablename__ = 'neighborhood_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    theft = Column('theft', Integer)
    date_occurrence = Column('date_occurrence', DateTime)
    neighborhood_id = Column('neighborhood_id', Integer, ForeignKey("ssp_go.neighborhood.id"))
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    neighborhood = relationship("Neighborhood", back_populates='neighborhood_quantity')


class District(Base):
    __tablename__ = 'district'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(190))
    geo_location = Column('geo_location', JSON)
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    district_quantity = relationship("DistrictQuantity", back_populates='district')


class DistrictQuantity(Base):
    __tablename__ = 'district_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = Column('id', Integer, primary_key=True)
    theft = Column('theft', Integer)
    date_occurrence = Column('date_occurrence', DateTime)
    district_id = Column('district_id', Integer, ForeignKey("ssp_go.district.id"))
    created_at = Column('created_at', DateTime, default=datetime.utcnow())

    district = relationship("District", back_populates='district_quantity')
