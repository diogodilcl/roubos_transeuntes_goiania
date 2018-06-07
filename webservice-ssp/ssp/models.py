from datetime import datetime

from ssp.common.database import db


class Base:

    def to_json(self):
        return self.__dict__


class City(db.Model, Base):
    __tablename__ = 'city'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    geo_location = db.Column('geo_location', db.JSON)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    city_quantities = db.relationship("CityQuantity", back_populates='city')


class CityQuantity(db.Model, Base):
    __tablename__ = 'city_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    theft = db.Column('theft', db.Integer)
    date_occurrence = db.Column('date_occurrence', db.DateTime)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    city = db.relationship("City", back_populates='city_quantities')
    city_id = db.Column('city_id', db.Integer, db.ForeignKey("ssp_go.city.id"))


class Neighborhood(db.Model, Base):
    __tablename__ = 'neighborhood'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    geo_location = db.Column('geo_location', db.JSON)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    neighborhood_quantity = db.relationship("NeighborhoodQuantity", back_populates='neighborhood')


class NeighborhoodQuantity(db.Model, Base):
    __tablename__ = 'neighborhood_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    theft = db.Column('theft', db.Integer)
    date_occurrence = db.Column('date_occurrence', db.DateTime)
    neighborhood_id = db.Column('neighborhood_id', db.Integer, db.ForeignKey("ssp_go.neighborhood.id"))
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    neighborhood = db.relationship("Neighborhood", back_populates='neighborhood_quantity')


class District(db.Model, Base):
    __tablename__ = 'district'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    geo_location = db.Column('geo_location', db.JSON)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    district_quantity = db.relationship("DistrictQuantity", back_populates='district')


class DistrictQuantity(db.Model, Base):
    __tablename__ = 'district_quantity'
    __table_args__ = {'schema': 'ssp_go'}

    id = db.Column('id', db.Integer, primary_key=True)
    theft = db.Column('theft', db.Integer)
    date_occurrence = db.Column('date_occurrence', db.DateTime)
    district_id = db.Column('district_id', db.Integer, db.ForeignKey("ssp_go.district.id"))
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())

    district = db.relationship("District", back_populates='district_quantity')
