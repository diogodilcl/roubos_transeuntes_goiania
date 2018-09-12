import logging
from http import HTTPStatus

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import NotFound

from config import APP_ENV
from ssp.common.database import db
from ssp.v1.neighborhood import neighborhood_bp
from ssp.v1.theft import theft_bp
from ssp.v2.neighborhood import neighborhood_v2_bp
from ssp.v2.theft import theft_v2_bp

application = Flask(__name__)

application.config.from_object('config.Config')

db.init_app(application)

application.register_blueprint(theft_bp, url_prefix='/v1/thefts')

application.register_blueprint(theft_v2_bp, url_prefix='/v2/thefts')

application.register_blueprint(neighborhood_bp, url_prefix='/v1/neighborhood')
application.register_blueprint(neighborhood_v2_bp, url_prefix='/v2/neighborhood')
logger = logging.getLogger(__name__)

CORS(application)


@application.errorhandler(Exception)
def handle_invalid_usage(e):
    logger.exception(e)
    error_description = "Internal server error"
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    response = jsonify({"error_description": error_description})
    response.status_code = status_code
    return response


@application.errorhandler(NotFound)
def not_found_exception(e):
    response = jsonify({"error_description": "Not found this resource."})
    response.status_code = HTTPStatus.NOT_FOUND
    return response


@application.route('/health')
def health():
    return jsonify({'message': 'ok'})


if __name__ == '__main__':
    application.debug = APP_ENV
    application.run(host='0.0.0.0')
    # application.run()
