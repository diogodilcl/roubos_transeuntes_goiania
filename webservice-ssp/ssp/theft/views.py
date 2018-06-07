import itertools
import operator
from datetime import datetime
from operator import itemgetter

import pandas
from flask import request, jsonify
from sqlalchemy import func, desc
from statsmodels.tsa.arima_model import ARIMAResults

from config import ROOT
from ssp.models import DistrictQuantity, District, CityQuantity, City, Neighborhood, NeighborhoodQuantity
from ssp.theft import theft_bp


@theft_bp.route("/cities")
def cities():
    start = request.args.get('start')
    end = request.args.get('end')
    rows = CityQuantity.query.join(City).with_entities(City.name, CityQuantity.date_occurrence,
                                                       CityQuantity.theft).filter(
        CityQuantity.date_occurrence >= start).filter(CityQuantity.date_occurrence <= end).all()
    values = __transform(rows)
    if datetime.strptime(start, '%Y-%m-%d') >= datetime.strptime('2018-01-01', '%Y-%m-%d'):
        loaded = ARIMAResults.load(ROOT + '/cities.pkl')
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
            NeighborhoodQuantity.date_occurrence <= end).order_by(desc("total")).limit(10).all()
        ids = [x.neighborhood_id for x in ids_to_query]
    rows = NeighborhoodQuantity.query.join(Neighborhood).with_entities(Neighborhood.name.label('name'),
                                                                       NeighborhoodQuantity.date_occurrence.label(
                                                                           'date'),
                                                                       NeighborhoodQuantity.theft.label(
                                                                           'theft')).filter(
        NeighborhoodQuantity.date_occurrence >= start).filter(
        NeighborhoodQuantity.date_occurrence < end).filter(NeighborhoodQuantity.neighborhood_id.in_(ids)).all()

    return jsonify(__transform(rows))


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
