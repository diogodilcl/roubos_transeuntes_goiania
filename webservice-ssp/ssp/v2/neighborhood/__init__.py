from flask import Blueprint

neighborhood_v2_bp = Blueprint('neighborhood_v2', __name__)

from . import views
