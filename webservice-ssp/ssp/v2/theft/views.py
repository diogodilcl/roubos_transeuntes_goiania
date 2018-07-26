import itertools
import operator
from datetime import datetime
from operator import itemgetter

import pandas
from flask import request, jsonify
from sqlalchemy import func, desc
from statsmodels.tsa.seasonal import seasonal_decompose

from ssp.v2.models_dw import FACT_thefts, DIM_city, DIM_time, DIM_district, DIM_neighborhood
from ssp.v2.theft import theft_v2_bp


@theft_v2_bp.route("/cities")
def cities():
    start = request.args.get('start')
    end = request.args.get('end')
    periodicity = request.args.get('periodicity')
    query = FACT_thefts.query.join(DIM_city) \
        .join(DIM_time)
    if start and end:
        query = query.filter(
            DIM_time.date_occur >= start).filter(DIM_time.date_occur <= end)
    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), 'DIM_city.name', 'DIM_time.year') \
            .with_entities(DIM_city.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'), DIM_time.year)
    else:
        query = query.with_entities(DIM_city.name, DIM_time.date_occur,
                                    FACT_thefts.theft)
    rows = query.all()
    values = __transform(rows, periodicity and periodicity != 'monthly')
    return jsonify(values)


@theft_v2_bp.route("/districts")
def districts():
    start = request.args.get('start')
    end = request.args.get('end')
    periodicity = request.args.get('periodicity')
    query = FACT_thefts.query.join(DIM_district) \
        .join(DIM_time).filter(
        DIM_time.date_occur >= start).filter(DIM_time.date_occur <= end)
    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), DIM_district.name) \
            .with_entities(DIM_district.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'))
    else:
        query = query.with_entities(DIM_district.name, DIM_time.date_occur,
                                    FACT_thefts.theft)
    rows = query.all()
    values = __transform(rows, periodicity and periodicity != 'monthly')
    return jsonify(values)


@theft_v2_bp.route("/districts/<type>")
def districts_trends(type):
    ## todo testar
    year = int(request.args.get('year'))
    start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
    end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()
    ids = request.args.getlist('ids', type=int)
    query = FACT_thefts.query.join(DIM_district).join(DIM_time).with_entities(FACT_thefts.date_occurrence.label('date'),
                                                                              DIM_district.name.label('name'),
                                                                              FACT_thefts.theft.label('theft')).filter(
        DIM_time.date_occur >= start).filter(
        DIM_time.date_occur <= end)
    if ids:
        query = query.filter(FACT_thefts.DIM_neighborhood_id.in_(ids))
    return jsonify(__to_analytics(query.all(), type))


@theft_v2_bp.route("/neighborhoods")
def general():
    ## todo testar
    start = request.args.get('start')
    end = request.args.get('end')
    ids = request.args.getlist('ids', type=int)
    if not ids:
        ids_to_query = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).with_entities(
            FACT_thefts.DIM_neighborhood_id.label('neighborhood_id'),
            func.sum(FACT_thefts.theft).label("total")).group_by(
            FACT_thefts.DIM_neighborhood_id).filter(
            DIM_time.date_occur >= start).filter(
            DIM_time.date_occur <= end).order_by(desc("total")).limit(5).all()
        ids = [x.neighborhood_id for x in ids_to_query]
    rows = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).with_entities(DIM_neighborhood.name.label('name'),
                                                                                 DIM_time.date_occur.label(
                                                                                     'date'),
                                                                                 FACT_thefts.theft.label(
                                                                                     'theft')).filter(
        DIM_time.date_occur >= start).filter(
        DIM_time.date_occur < end).filter(FACT_thefts.DIM_neighborhood_id.in_(ids)).all()

    return jsonify(__transform(rows))


@theft_v2_bp.route("/neighborhoods/<type>")
def neighborhoods_trends(type):
    ## todo testar
    year = int(request.args.get('year'))
    start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
    end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()
    ids = request.args.getlist('ids', type=int)
    if not ids:
        ids_to_query = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).with_entities(
            FACT_thefts.DIM_neighborhood_id.label('neighborhood_id'),
            func.sum(FACT_thefts.theft).label("total")).group_by(
            FACT_thefts.DIM_neighborhood_id).filter(
            DIM_time.date_occur >= start).filter(
            DIM_time.date_occur <= end).order_by(desc("total")).limit(5).all()
        ids = [x.neighborhood_id for x in ids_to_query]
    rows = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).with_entities(DIM_neighborhood.name.label('name'),
                                                                                 DIM_time.date_occur.label(
                                                                                     'date'),
                                                                                 FACT_thefts.theft.label(
                                                                                     'theft')).filter(
        DIM_time.date_occur >= start).filter(
        DIM_time.date_occur < end).filter(FACT_thefts.DIM_neighborhood_id.in_(ids)).all()

    return jsonify(__to_analytics(rows, type))


def __transform(rows, periodicity=False):
    data = []
    total_general = 0
    labels = list()
    if periodicity:
        for key, value in itertools.groupby(sorted(rows, key=operator.itemgetter(1)), key=operator.itemgetter(1)):
            labels.append(key)
        # grouper = itemgetter(1, 3)
        # for key, value in itertools.groupby(sorted(rows, key=grouper),
        #                                     key=grouper):
        #     labels.append(key)
        ## todo fazer labels para periodicity para multiplos anos
    else:
        for key, value in itertools.groupby(sorted(rows, key=operator.itemgetter(1)), key=operator.itemgetter(1)):
            labels.append(key.strftime('%Y-%m'))

    for key, value in itertools.groupby(sorted(rows, key=itemgetter(0)), key=itemgetter(0)):
        thefts = []
        total = 0
        for i in sorted(value, key=operator.itemgetter(1), reverse=False):
            thefts.append(int(i.theft))
            total += int(i.theft)
        data.append({"values": thefts, "label": key, "total": total})
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
        group.drop('name', axis=1, inplace=True)
        group = group.sort_index()
        result = seasonal_decompose(group, freq=12, model='additive')
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
