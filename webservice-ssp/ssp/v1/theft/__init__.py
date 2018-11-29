from flask import Blueprint

theft_bp = Blueprint('theft', __name__)

from . import views
