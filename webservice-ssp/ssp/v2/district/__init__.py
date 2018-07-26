from flask import Blueprint

district_v2_bp = Blueprint('district_v2', __name__)

from . import views
