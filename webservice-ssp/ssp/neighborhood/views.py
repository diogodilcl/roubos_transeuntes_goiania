from flask import json

from ssp.models import Neighborhood
from ssp.neighborhood import neighborhood_bp


@neighborhood_bp.route("")
def neighborhood():
    neighborhoods = [{"id": x.id, "name": x.name} for x in
                     Neighborhood.query.with_entities(Neighborhood.id, Neighborhood.name).all()]
    return json.dumps(neighborhoods)
