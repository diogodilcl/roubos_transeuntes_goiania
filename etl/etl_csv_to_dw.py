import calendar
import datetime

import pandas as pd

from database import Database
from models import Neighborhood, NeighborhoodQuantity, District, DistrictQuantity
from models_dw import DIM_time, FACT_thefts, DIM_city, DIM_neighborhood, DIM_district


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


DATE_START = datetime.date(2010, 1, 1)
DATE_END = datetime.date(2018, 7, 1)

current = DATE_START

db = Database()
## data (YYYY-MM-DD), nome, quantidade
df_city = pd.read_csv('cidade.csv', index_col=0, parse_dates=True).sort_index()
df_district = pd.read_csv('zonas.csv', index_col=0, parse_dates=True).sort_index()
df_neighborhoods = pd.read_csv('distritos.csv', index_col=0, parse_dates=True).sort_index()

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
        grouped = df_city.groupby('nome')
        for name, group in grouped:
            dim_city_save = DIM_city(name=name)
            session.add(dim_city_save)
            for index, row in group.iterrows():
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(index.year, index.month, index.day)),
                    DIM_city_id=dim_city_save.id, theft=row['quantidade'])
                session.add(fact_thefts_save)
        session.commit()
    except Exception as e:
        print(e)

    try:
        grouped = df_district.groupby('nome')
        for name, group in grouped:
            dim_district_save = DIM_district(name=name)
            session.add(dim_district_save)
            for index, row in group.iterrows():
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(index.year, index.month, index.day)),
                    DIM_district_id=dim_district_save.id, theft=row['quantidade'])
                session.add(fact_thefts_save)
        session.commit()
    except Exception as e:
        print(e)

    try:
        grouped = df_neighborhoods.groupby('nome')
        for name, group in grouped:
            dim_neighborhood_save = DIM_neighborhood(name=name)
            session.add(dim_neighborhood_save)
            for index, row in group.iterrows():
                fact_thefts_save = FACT_thefts(
                    DIM_time_id=int('{}{}{}'.format(index.year, index.month, index.day)),
                    DIM_neighborhood_id=dim_neighborhood_save.id, theft=row['quantidade'])
                session.add(fact_thefts_save)
        session.commit()
    except Exception as e:
        print(e)
