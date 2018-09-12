from datetime import datetime

import pandas
from flask import request, jsonify
from sqlalchemy import func, desc
from statsmodels.tsa.seasonal import seasonal_decompose

from ssp.common.bool_utils import str_to_bool
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
        query = query.with_entities(DIM_city.name, DIM_time.date_occur.label('date'),
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
        .join(DIM_time)
    if start and end:
        query = query.filter(
            DIM_time.date_occur >= start).filter(DIM_time.date_occur <= end)
    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), DIM_district.name, DIM_time.year) \
            .with_entities(DIM_district.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'), DIM_time.year)
    else:
        query = query.with_entities(DIM_district.name, DIM_time.date_occur.label('date'),
                                    FACT_thefts.theft)
    rows = query.all()
    values = __transform(rows, periodicity and periodicity != 'monthly')
    return jsonify(values)


@theft_v2_bp.route("/districts/<type>")
def districts_trends(type):
    year = request.args.get('year')
    start = None
    end = None
    model = str_to_bool(request.args.get('model'))
    ids = request.args.getlist('ids', type=int)
    periodicity = request.args.get('periodicity', default='monthly')

    if year:
        year = int(request.args.get('year'))
        start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
        end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()

    query = FACT_thefts.query.join(DIM_district).join(DIM_time)
    if ids:
        query = query.filter(FACT_thefts.DIM_neighborhood_id.in_(ids))
    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), DIM_district.name, DIM_time.year) \
            .with_entities(DIM_district.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'), DIM_time.year)
    else:
        query = query.with_entities(DIM_time.date_occur.label('date'),
                                    DIM_district.name.label('name'),
                                    FACT_thefts.theft.label('theft'))
    if start and end:
        query = query.filter(
            DIM_time.date_occur >= start).filter(
            DIM_time.date_occur <= end)
    return jsonify(__to_analytics(query.all(), type, periodicity, model))


@theft_v2_bp.route("/neighborhoods")
def general():
    start = request.args.get('start')
    end = request.args.get('end')
    ids = request.args.getlist('ids', type=int)
    periodicity = request.args.get('periodicity')
    query = FACT_thefts.query.join(DIM_neighborhood) \
        .join(DIM_time)

    if not ids:
        query_ids = FACT_thefts.query
        if start and end:
            query_ids = query_ids.filter(
                DIM_time.date_occur >= start).filter(
                DIM_time.date_occur <= end)
        query_ids = query_ids.join(DIM_neighborhood).join(DIM_time).with_entities(
            FACT_thefts.DIM_neighborhood_id.label('neighborhood_id'),
            func.sum(FACT_thefts.theft).label("total")).group_by(
            FACT_thefts.DIM_neighborhood_id).order_by(desc("total")).order_by(DIM_time.date_occur.asc()).limit(5)

        ids_to_query = query_ids.all()
        ids = [x.neighborhood_id for x in ids_to_query]

    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), DIM_neighborhood.name, DIM_time.year) \
            .with_entities(DIM_neighborhood.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'), DIM_time.year)
    else:
        query = query.with_entities(DIM_neighborhood.name, DIM_time.date_occur.label('date'),
                                    FACT_thefts.theft)

    query = query.filter(
        FACT_thefts.DIM_neighborhood_id.in_(ids))

    if start and end:
        query = query.filter(
            DIM_time.date_occur >= start).filter(DIM_time.date_occur <= end)
    rows = query.all()
    return jsonify(__transform(rows, periodicity and periodicity != 'monthly'))


@theft_v2_bp.route("/neighborhoods/<type>")
def neighborhoods_trends(type):
    year = request.args.get('year')
    start = None
    end = None
    model = str_to_bool(request.args.get('model'))
    ids = request.args.getlist('ids', type=int)
    periodicity = request.args.get('periodicity', default='monthly')

    if year:
        year = int(request.args.get('year'))
        start = datetime.strptime('{}-01-01'.format(year - 2), '%Y-%m-%d').date()
        end = datetime.strptime('{}-12-30'.format(year), '%Y-%m-%d').date()

    if not ids:
        query_ids = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).with_entities(
            FACT_thefts.DIM_neighborhood_id.label('neighborhood_id'),
            func.sum(FACT_thefts.theft).label("total")).group_by(
            FACT_thefts.DIM_neighborhood_id)
        if year:
            query_ids = query_ids.filter(
                DIM_time.date_occur >= start).filter(
                DIM_time.date_occur <= end)

        ids_to_query = query_ids.order_by(desc("total")).limit(5).all()
        ids = [x.neighborhood_id for x in ids_to_query]

    query = FACT_thefts.query.join(DIM_neighborhood).join(DIM_time).filter(
        FACT_thefts.DIM_neighborhood_id.in_(ids))

    if year:
        query = query.filter(
            DIM_time.date_occur >= start).filter(
            DIM_time.date_occur < end)
    if periodicity and periodicity != 'monthly':
        query = query.group_by('DIM_time.{}'.format(periodicity), DIM_neighborhood.name, DIM_time.year) \
            .with_entities(DIM_neighborhood.name, 'DIM_time.{}'.format(periodicity),
                           func.sum(FACT_thefts.theft).label(
                               'theft'), DIM_time.year)
    else:
        query = query.with_entities(DIM_neighborhood.name.label('name'),
                                    DIM_time.date_occur.label(
                                        'date'),
                                    FACT_thefts.theft.label(
                                        'theft'))
    rows = query.all()

    return jsonify(__to_analytics(rows, type, periodicity, model))


def __transform(rows, periodicity=False):
    rows_tuple = list()
    if periodicity:
        for current in rows:
            date = datetime.strptime('{}-0{}-01'.format(current[3], current[1]), '%Y-%m-%d').date()
            tuple = {"date": date, "name": current[0], "theft": int(current[2])}
            rows_tuple.append(tuple)
    else:
        rows_tuple = list(rows)
    df = pandas.DataFrame(rows_tuple)
    df = df.set_index('date').sort_index()
    data = []
    labels = list()
    total_general = 0
    index_df = sorted(list(set(df.index)))

    for key in index_df:
        labels.append(key.strftime('%Y-%m'))

    for name, group in df.groupby('name'):
        group.drop('name', axis=1, inplace=True)
        thefts = []
        total = 0
        for value in index_df:
            val = 0
            if value in group.index:
                val = group.loc[value].item()
            thefts.append(val)
            total += val
        data.append({"values": thefts, "label": name, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}


def __to_analytics(rows, type, periodicity='monthly', model=True):
    period = {
        "monthly": 12,
        "quarter": 4,
        "semester": 2
    }
    ## todo analizar quando saão todos os anos e mensal e multiplicativo
    rows_tuple = list()
    if periodicity and periodicity != 'monthly':
        for current in rows:
            date = datetime.strptime('{}-0{}-01'.format(current[3], current[1]), '%Y-%m-%d').date()
            tuple = {"date": date, "name": current[0], "theft": int(current[2])}
            rows_tuple.append(tuple)
    else:
        rows_tuple = list(rows)
    df = pandas.DataFrame(rows_tuple)
    df = df.set_index('date').sort_index()
    data = []
    total_general = 0
    labels = list()
    type_model = 'additive' if model else 'multiplicative'
    # index_df = sorted(list(set(df.index)))

    for name, group in df.groupby('name'):
        group.drop('name', axis=1, inplace=True)
        group = group.sort_index()
        result = seasonal_decompose(group, freq=period[periodicity], model=type_model)
        variable = getattr(result, type)
        result_sort = variable.sort_index()
        result_sort.dropna(inplace=True)
        thefts = []

        labels = list()
        for key, value in result_sort.groupby(['date']):
            labels.append(key.strftime('%Y-%m'))

        total = 0
        for value in result_sort.values:
            val = float("{0:.4f}".format(value[0]))
            thefts.append(val)
            total += val

        data.append({"values": thefts, "label": name, "total": total})
        total_general += total

    return {"labels": labels, "data": data, "total": total_general}
