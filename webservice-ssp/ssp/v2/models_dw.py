from datetime import datetime

from sqlalchemy.orm import relationship

from ssp.common.database import db


class Base:

    def to_json(self):
        return self.__dict__


class DIM_city(db.Model, Base):
    __tablename__ = 'DIM_city'
    __table_args__ = {'schema': 'tcc'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_city')


class DIM_district(db.Model, Base):
    __tablename__ = 'DIM_district'
    __table_args__ = {'schema': 'tcc'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_district')


class DIM_neighborhood(db.Model, Base):
    __tablename__ = 'DIM_neighborhood'
    __table_args__ = {'schema': 'tcc'}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(190))
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_neighborhood')


class DIM_time(db.Model, Base):
    __tablename__ = 'DIM_time'
    __table_args__ = {'schema': 'tcc'}

    time_key = db.Column('time_key', db.Integer, primary_key=True)
    date_occur = db.Column('date_occur', db.Date, default=datetime.utcnow())
    month = db.Column('month', db.Integer)
    year = db.Column('year', db.Integer)
    quarter = db.Column('quarter', db.Integer)
    semester = db.Column('semester', db.Integer)
    FACT_thefts = relationship("FACT_thefts", back_populates='dim_time')


class FACT_thefts(db.Model, Base):
    __tablename__ = 'FACT_thefts'
    __table_args__ = {'schema': 'tcc'}

    id = db.Column('id', db.Integer, primary_key=True)
    DIM_time_id = db.Column('DIM_time_id', db.Integer, db.ForeignKey("tcc.DIM_time.time_key"))
    DIM_neighborhood_id = db.Column('DIM_neighborhood_id', db.Integer, db.ForeignKey("tcc.DIM_neighborhood.id"), default=None,
                                 nullable=True)
    DIM_district_id = db.Column('DIM_district_id', db.Integer, db.ForeignKey("tcc.DIM_district.id"), default=None,
                             nullable=True)
    DIM_city_id = db.Column('DIM_city_id', db.Integer, db.ForeignKey("tcc.DIM_city.id"), default=None, nullable=True)
    theft = db.Column('theft', db.Integer)

    dim_time = relationship("DIM_time", back_populates='FACT_thefts')
    dim_neighborhood = relationship("DIM_neighborhood", back_populates='FACT_thefts')
    dim_district = relationship("DIM_district", back_populates='FACT_thefts')
    dim_city = relationship("DIM_city", back_populates='FACT_thefts')
