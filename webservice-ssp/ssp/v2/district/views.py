from flask import json, request

from ssp.v2.district import district_v2_bp
from ssp.v2.models_dw import DIM_district


@district_v2_bp.route("")
def neighborhood():
    districts = [{"id": x.id, "name": x.name} for x in
                 DIM_district.query.with_entities(DIM_district.id, DIM_district.name).all()]
    return json.dumps(districts)


@district_v2_bp.route("search")
def neighborhood_search():
    name = request.args.get('name')
    neighborhoods = DIM_district.query.with_entities(
        DIM_district.id.label('id'), DIM_district.name.label('name'),
    ).filter(DIM_district.name.like('%' + name + '%')).order_by(
        DIM_district.name).all()

    result = [{"id": x.id, "name": x.name} for x in neighborhoods]
    return json.dumps(result)
