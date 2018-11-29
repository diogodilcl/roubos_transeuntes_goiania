import calendar
import datetime

import pandas as pd

from database import Database
from models import City, CityQuantity, Neighborhood, NeighborhoodQuantity, District, DistrictQuantity
from models_dw import DIM_time, FACT_thefts, DIM_city, DIM_neighborhood, DIM_district


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


DATE_START = datetime.date(2010, 1, 1)
DATE_END = datetime.date(2018, 12, 1)

current = DATE_START

db = Database()
with db.db_session() as session:
    try:
        while current <= DATE_END:
            semester = 1
            if current.month >= 7:
                semester = 2
            save = DIM_time(time_key=int('{}{}{}'.format(current.year, current.month, current.day)), date_occur=current,
                            month=current.month, year=current.year, quarter=pd.Timestamp(current).quarter,
                            semester=semester)
            session.add(save)
            current = add_months(current, 1)
        session.commit()
    except Exception as e:
        print(e)

    try:
        cities = session.query(City).all()
        for current in cities:
            cities_quantities = session.query(CityQuantity).filter(
                CityQuantity.city_id == current.id).all()
            dim_city_save = DIM_city(id=current.id, name=current.name)
            session.add(dim_city_save)
            for child in cities_quantities:
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(child.date_occurrence.year, child.date_occurrence.month,
                                                    child.date_occurrence.day)),
                    DIM_city_id=dim_city_save.id, theft=child.theft)
                session.add(fact_thefts_save)
        session.commit()
    except Exception as e:
        print(e)

    try:
        districts = session.query(District).all()
        for current in districts:
            districts_quantities = session.query(DistrictQuantity).filter(
                DistrictQuantity.district_id == current.id).all()
            dim_district_save = DIM_district(id=current.id, name=current.name)
            session.add(dim_district_save)
            for child in districts_quantities:
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(child.date_occurrence.year, child.date_occurrence.month,
                                                    child.date_occurrence.day)),
                    DIM_district_id=dim_district_save.id, theft=child.theft)
                session.add(fact_thefts_save)
        session.commit()
    except Exception as e:
        print(e)

    try:
        neighborhoods = session.query(Neighborhood).all()
        for current in neighborhoods:
            neighborhood_quantities = session.query(NeighborhoodQuantity).filter(
                NeighborhoodQuantity.neighborhood_id == current.id).all()
            dim_neighborhood_save = DIM_neighborhood(id=current.id, name=current.name)
            session.add(dim_neighborhood_save)
            for child in neighborhood_quantities:
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(child.date_occurrence.year, child.date_occurrence.month,
                                                    child.date_occurrence.day)),
                    DIM_neighborhood_id=dim_neighborhood_save.id, theft=child.theft)
                session.add(fact_thefts_save)
            session.commit()
    except Exception as e:
        print(e)

# print(current.year)
#         print(pd.Timestamp(current).quarter)
#         print(pd.Timestamp(current).month)
#         semester = 1
#         if pd.Timestamp(current).month >= 7:
#             semester = 2
#         current = add_months(current, 1)
