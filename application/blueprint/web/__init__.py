from flask import Blueprint

web_bp = Blueprint('web', __name__, url_prefix='/web')

from . import chat