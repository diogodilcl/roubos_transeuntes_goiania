from flask import json, request

from ssp.v1.models import Neighborhood
from ssp.v1.neighborhood import neighborhood_bp


@neighborhood_bp.route("")
def neighborhood():
    neighborhoods = [{"id": x.id, "name": x.name} for x in
                     Neighborhood.query.with_entities(Neighborhood.id, Neighborhood.name).all()]
    return json.dumps(neighborhoods)


@neighborhood_bp.route("search")
def neighborhood_search():
    name = request.args.get('name')
    neighborhoods = Neighborhood.query.with_entities(
        Neighborhood.id.label('id'), Neighborhood.name.label('name'),
    ).filter(Neighborhood.name.like('%' + name + '%')).order_by(
        Neighborhood.name).all()

    result = [{"id": x.id, "name": x.name} for x in neighborhoods]
    return json.dumps(result)
