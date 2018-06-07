import logging
from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

from config import APP_ENV
from ssp.common.database import db
from ssp.neighborhood import neighborhood_bp
from ssp.theft import theft_bp

app = Flask(__name__)

app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(theft_bp, url_prefix='/v1/thefts')

app.register_blueprint(neighborhood_bp, url_prefix='/v1/neighborhood')

logger = logging.getLogger(__name__)


@app.errorhandler(Exception)
def handle_invalid_usage(e):
    logger.exception(e)
    error_description = "Internal server error"
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    response = jsonify({"error_description": error_description})
    response.status_code = status_code
    return response


@app.errorhandler(NotFound)
def not_found_exception(e):
    response = jsonify({"error_description": "Not found this resource."})
    response.status_code = HTTPStatus.NOT_FOUND
    return response


@app.route('/health')
def health():
    return jsonify({'message': 'ok'})


if __name__ == '__main__':
    app.debug = APP_ENV
    app.run()
