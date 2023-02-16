from flask import Blueprint

wechat_bp = Blueprint('wechat', __name__, url_prefix='/wechat')

from . import views
