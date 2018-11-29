import itertools
import operator
from datetime import datetime
from operator import itemgetter

import pandas
from flask import request, jsonify
from sqlalchemy import func, desc
from statsmodels.tsa.arima_model import ARIMAResults
from statsmodels.tsa.seasonal import seasonal_decompose

from config import ROOT
from ssp.v1.models import DistrictQuantity, District, CityQuantity, City, Neighborhood, NeighborhoodQuantity
from ssp.v1.theft import theft_bp


@theft_bp.route("/cities")
def cities():
    start = request.args.get('start')
    end = request.args.get('end')
    rows = CityQuantity.query.join(City).with_entities(City.name, CityQuantity.date_occurrence,
                                                       CityQuantity.theft).filter(
        CityQuantity.date_occurrence >= start).filter(CityQuantity.date_occurrence <= end).all()
    values = __transform(rows)
    if datetime.strptime(start, '%Y-%m-%d') >= datetime.strptime('2018-01-01', '%Y-%m-%d'):
        loaded = ARIMAResults.load(ROOT + 'ssp/v1/cities.pkl')
        d = pandas.date_range(start='1/1/2018', end='12/1/2018', freq='MS')
        d = d.format(formatter=lambda current: current.strftime('%Y-%m'))
        x = [int(round(x)) for x in loaded.forecast(steps=12)[0]]
        total = sum(x)
        values["labels"] = d
        values["total"] = values["total"] + total
        values["data"].append({"values": x, "label": "Goiânia Previsão", "total": total})
    return jsonify(values)


@theft_bp.route("/districts")
def districts():
    start = request.args.get('start')
    end = request.args.get('end')
    rows = DistrictQuantity.query.join(District).with_entities(District.name.label('name'),
                                                               DistrictQuantity.date_occurrence.label('date'),
                                                               DistrictQuantity.theft.label('theft')).filter(
        DistrictQuantity.date_occurrence >= start).filter(
        DistrictQuantity.date_occurrence <= end).all()
    values = __transform(rows)
    if datetime.strptime(start, '%Y-%m-%d') >= datetime.strptime('2018-01-01', '%Y-%m-%d'):
        d = pandas.date_range(start='1/1/2018', end='12/1/2018', freq='MS')
        d = d.format(formatter=lambda current: current.strftime('%Y-%m'))
        values["labels"] = d
        for row in District.query.with_entities(District.id.label('id'), District.name.label('name')).all():
            loaded = ARIMAResults.load(ROOT + '/{}.pkl'.format(row.id))
            x = [int(round(x)) for x in loaded.forecast(steps=12)[0]]
            total = sum(x)
            values["total"] += total
            values["data"].append({"values": x, "label": "{} Previsão".format(row.name), "total": total})
    return jsonify(values)


@theft_bp.route("/districts/<type>")
def districts_trends(type):
    year = int(request.args.get('year'))
    start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
    end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()
    rows = DistrictQuantity.query.join(District).with_entities(DistrictQuantity.date_occurrence.label('date'),
                                                               District.name.label('name'),
                                                               DistrictQuantity.theft.label('theft')).filter(
        DistrictQuantity.date_occurrence >= start).filter(
        DistrictQuantity.date_occurrence <= end).all()

    return jsonify(__to_analytics(rows, type))


@theft_bp.route("/neighborhoods")
def general():
    start = request.args.get('start')
    end = request.args.get('end')
    ids = request.args.getlist('ids', type=int)
    if not ids:
        ids_to_query = NeighborhoodQuantity.query.with_entities(
            NeighborhoodQuantity.neighborhood_id.label('neighborhood_id'),
            func.sum(NeighborhoodQuantity.theft).label("total")).group_by(
            NeighborhoodQuantity.neighborhood_id).filter(
            NeighborhoodQuantity.date_occurrence >= start).filter(
            NeighborhoodQuantity.date_occurrence <= end).order_by(desc("total")).limit(5).all()
        ids = [x.neighborhood_id for x in ids_to_query]
    rows = NeighborhoodQuantity.query.join(Neighborhood).with_entities(Neighborhood.name.label('name'),
                                                                       NeighborhoodQuantity.date_occurrence.label(
                                                                           'date'),
                                                                       NeighborhoodQuantity.theft.label(
                                                                           'theft')).filter(
        NeighborhoodQuantity.date_occurrence >= start).filter(
        NeighborhoodQuantity.date_occurrence < end).filter(NeighborhoodQuantity.neighborhood_id.in_(ids)).all()

    return jsonify(__transform(rows))


@theft_bp.route("/neighborhoods/<type>")
def neighborhoods_trends(type):
    year = int(request.args.get('year'))
    start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
    end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()
    ids = request.args.getlist('ids', type=int)
    if not ids:
        ids_to_query = NeighborhoodQuantity.query.with_entities(
            NeighborhoodQuantity.neighborhood_id.label('neighborhood_id'),
            func.sum(NeighborhoodQuantity.theft).label("total")).group_by(
            NeighborhoodQuantity.neighborhood_id).filter(
            NeighborhoodQuantity.date_occurrence >= start).filter(
            NeighborhoodQuantity.date_occurrence <= end).order_by(desc("total")).limit(5).all()
        ids = [x.neighborhood_id for x in ids_to_query]
    rows = NeighborhoodQuantity.query.join(Neighborhood).with_entities(NeighborhoodQuantity.date_occurrence.label(
        'date'),
        Neighborhood.name.label('name'),
        NeighborhoodQuantity.theft.label(
            'theft')).filter(
        NeighborhoodQuantity.date_occurrence >= start).filter(
        NeighborhoodQuantity.date_occurrence < end).filter(NeighborhoodQuantity.neighborhood_id.in_(ids)).all()

    return jsonify(__to_analytics(rows, type))


def __transform(rows):
    data = []
    total_general = 0
    labels = list()
    for key, value in itertools.groupby(sorted(rows, key=operator.itemgetter(1)), key=operator.itemgetter(1)):
        labels.append(key.strftime('%Y-%m'))
    # for key, value in itertools.groupby(rows, key=itemgetter(1)):
    #     labels.add(key.strftime('%Y-%m'))

    for key, value in itertools.groupby(rows, key=itemgetter(0)):
        thefts = []
        total = 0
        for i in sorted(value, key=operator.itemgetter(1), reverse=False):
            thefts.append(i.theft)
            total += i.theft
        data.append({"values": thefts, "label": key, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}


def __transform_from_pandas(rows):
    data = []
    total_general = 0
    labels = list()
    for key, value in rows.groupby(['date']):
        labels.append(key.strftime('%Y-%m'))

    for key, value in rows.groupby(['name']):
        thefts = []
        total = 0
        for i in sorted(value, key=operator.itemgetter(0), reverse=False):
            thefts.append(i.theft)
            total += i.theft
        data.append({"values": thefts, "label": key, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}


# def __to_trend(rows):
#     df = pandas.DataFrame(list(rows))
#     df = df.set_index('date').sort_index()
#     df_concat = pandas.DataFrame()
#     grouped = df.groupby('name')
#     for name, group in grouped:
#         group = group.sort_index()
#         group.drop('name', axis=1, inplace=True)
#         result = seasonal_decompose(group, model='additive')
#
#         df2 = pandas.DataFrame(result.trend)
#         df2['name'] = name
#         df_concat = pandas.concat([df_concat, df2], axis=1)
#
#     df_concat.dropna(inplace=True)
#     df_concat = df_concat.sort_index()
#     # df_concat['date'] = df_concat.index
#     # df = pandas.DataFrame(df_concat[['name', 'date', 'theft']])
#     return df_concat
#     # return map(tuple, df.values)
#     # return list(zip(df["name"], df["date"], df["theft"]))
#     # return list(df_concat.itertuples())


def __to_trend(rows):
    df = pandas.DataFrame(list(rows))
    df = df.set_index('date').sort_index()
    data = []
    total_general = 0
    labels = list()

    for name, group in df.groupby('name'):
        labels = list()
        group = group.sort_index()
        group.drop('name', axis=1, inplace=True)
        result = seasonal_decompose(group, model='additive')
        result_sort = result.trend.sort_index()
        result_sort.dropna(inplace=True)
        for key, value in result_sort.groupby(['date']):
            labels.append(key.strftime('%Y-%m'))
        thefts = []
        total = 0
        for value in result_sort.values:
            val = float("{0:.2f}".format(value[0]))
            thefts.append(val)
            total += val
        data.append({"values": thefts, "label": name, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}


def __to_analytics(rows, type):
    df = pandas.DataFrame(list(rows))
    df = df.set_index('date').sort_index()
    data = []
    total_general = 0
    labels = list()

    for name, group in df.groupby('name'):
        labels = list()
        group = group.sort_index()
        group.drop('name', axis=1, inplace=True)
        result = seasonal_decompose(group, model='additive')
        variable = getattr(result, type)
        result_sort = variable.sort_index()
        result_sort.dropna(inplace=True)
        for key, value in result_sort.groupby(['date']):
            labels.append(key.strftime('%Y-%m'))
        thefts = []
        total = 0
        for value in result_sort.values:
            val = float("{0:.4f}".format(value[0]))
            thefts.append(val)
            total += val
        data.append({"values": thefts, "label": name, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}


def __to_resid(rows):
    df = pandas.DataFrame(list(rows))
    df = df.set_index('date').sort_index()
    data = []
    total_general = 0
    labels = list()

    for name, group in df.groupby('name'):
        labels = list()
        group = group.sort_index()
        group.drop('name', axis=1, inplace=True)
        result = seasonal_decompose(group, model='additive')
        result_sort = result.resid.sort_index()
        result_sort.dropna(inplace=True)
        for key, value in result_sort.groupby(['date']):
            labels.append(key.strftime('%Y-%m'))
        thefts = []
        total = 0
        for value in result_sort.values:
            val = float("{0:.2f}".format(value[0]))
            thefts.append(val)
            total += val
        data.append({"values": thefts, "label": name, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}
