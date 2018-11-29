from flask import Blueprint

theft_v2_bp = Blueprint('theft_v2_bp', __name__)

from . import views
