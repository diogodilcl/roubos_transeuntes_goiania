from flask import json, request

from ssp.v2.models_dw import DIM_neighborhood
from ssp.v2.neighborhood import neighborhood_v2_bp


@neighborhood_v2_bp.route("")
def neighborhood():
    neighborhoods = [{"id": x.id, "name": x.name} for x in
                     DIM_neighborhood.query.with_entities(DIM_neighborhood.id, DIM_neighborhood.name).all()]
    return json.dumps(neighborhoods)


@neighborhood_v2_bp.route("search")
def neighborhood_search():
    name = request.args.get('name')
    neighborhoods = DIM_neighborhood.query.with_entities(
        DIM_neighborhood.id.label('id'), DIM_neighborhood.name.label('name'),
    ).filter(DIM_neighborhood.name.like('%' + name + '%')).order_by(
        DIM_neighborhood.name).all()

    result = [{"id": x.id, "name": x.name} for x in neighborhoods]
    return json.dumps(result)
