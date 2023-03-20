import datetime
import logging.config
import os
import sys
import time
from importlib import import_module
from logging import StreamHandler
from flask.json import JSONEncoder
import enum
import decimal
from pydantic import BaseModel as PydanticModel
from flask import Flask, request, g
from flask_siwadoc import ValidationError
from werkzeug.exceptions import HTTPException

from application.cli import configure_cli
from application.config import config, BaseConfig
from application.utils import request_utils
from application.utils.response_utils import error

__all__ = ['create_app']


def create_app(config_name=None, app_name=None):
    """使用工厂模式创建app"""
    if not app_name:
        app_name = __name__
    app = Flask(app_name)
    configure_app(app, config_name)
    configure_logging(app)
    config_blueprint(app)
    config_extensions(app)
    configure_hook(app)
    configure_json_decode(app)
    configure_errors(app)
    configure_cli(app)

    return app


def configure_app(app, config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])


def config_blueprint(app):
    from application.blueprint.wechat import wechat_bp
    app.register_blueprint(wechat_bp)


def config_extensions(app):
    """
    配置扩展
    """
    # 在方法里面import主要是为了先配置logging，否则在下面模块中如有引用了logging，那么在app设置的logger配置将不在生效
    from application.extensions import siwa, openai_api, cache
    # 根据models生成rest api前， 必须import 所有model
    local_all_models(app)
    siwa.init_app(app)
    openai_api.init_app(app)
    cache.init_app(app)



def configure_logging(app):
    """配置日志
    """
    # 清除掉默认handlers
    app.logger.handlers = []
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.disabled = True
    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.handlers = []
    sqlalchemy_logger.propagate = False
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.logger.propagate = False

    stream_handler = StreamHandler(sys.stdout)
    log_level_str = app.config.get('LOG_LEVEL', None) or 'DEBUG'
    log_level = getattr(logging, log_level_str)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)
    api_logger = logging.getLogger("application")
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    api_logger.handlers = [stream_handler]
    # api_logger.handlers.extend(gunicorn_logger.handlers)
    api_logger.propagate = False


def configure_hook(app):
    @app.before_request
    def before_request():
        g.start = time.time()
        if request.data:
            try:
                app.logger.info("request body: %s", request.data)
            except:
                import traceback
                traceback.print_exc()

    @app.after_request
    def log_response(response):
        diff = int((time.time() - g.start) * 1000)
        app.logger.info("%s %s %s %s %sms",
                        *[request_utils.get_client_ip(), request.method, request.full_path, response.status,
                          diff])
        return response


def configure_errors(app):
    from application.errors import ApiError

    @app.errorhandler(ApiError)
    def api_error(e: ApiError):
        app.logger.warning(f"\ncode={e.code}\nmsg:{e.msg} \nerror_info:{e.error_info}")
        return error(code=e.code, msg=e.msg, http_code=e.http_code, data=e.data, error_info=e.error_info)

    @app.errorhandler(ValidationError)
    def validate_error(e: ValidationError):
        app.logger.warning(f"validate error info:{e.errors()}")
        return error(code=1002, msg="请求参数错误", http_code=400, data=None, error_info=e.errors())

    @app.errorhandler(HTTPException)
    def http_error(e):
        response = e.get_response()
        return error(msg=str(e),
                     http_code=response.status_code,
                     code=response.status_code)

    @app.errorhandler(Exception)
    def server_error(e):
        app.logger.error(f"内部错误：{str(e)}", exc_info=True)
        return error(code=500, http_code=500, msg="内部错误")


def configure_json_decode(app):
    class CustomJSONEncoder(JSONEncoder):

        def default(self, obj):
            try:
                if isinstance(obj, PydanticModel):
                    return obj.dict()
                elif isinstance(obj, enum.Enum):
                    return obj.value
                elif type(obj) is datetime.date:
                    return datetime.datetime(obj.year, obj.month, obj.day).isoformat()
                elif type(obj) is datetime.datetime:
                    return obj.isoformat()
                elif type(obj) is datetime.time:
                    return str(obj)
                elif isinstance(obj, decimal.Decimal):
                    return float(obj)
                # 时间区间
                elif isinstance(obj, datetime.timedelta):
                    return int(obj.total_seconds() * 1000)
                else:
                    return str(obj)
            except TypeError:
                pass
            return JSONEncoder.default(self, obj)

    app.json_encoder = CustomJSONEncoder


def local_all_models(app):
    """
    加载所有的models
    """
    root_path = app.root_path
    models_directory = os.path.join(root_path, 'application/models')
    for root, dirs, files in os.walk(models_directory):
        namespace = 'application.models'
        if 'celery_app.py' not in files:
            continue

        root = root.replace(models_directory, "", 1)
        path = root.split(os.sep)
        for file in files:
            if not file.endswith('.py'):
                continue
            module_paths = [namespace] + path[1:]
            if file != 'celery_app.py':
                module_name = os.path.splitext(file)[0]
                module_paths = module_paths + [module_name]

            model_module = '.'.join(module_paths)
            import_module(model_module)


def configure_jwt(jwt_ext):
    @jwt_ext.user_lookup_loader
    def loader_user_callback(jwt_headers, jwt_payload):
        identity = jwt_payload.get("sub")
        from application.utils.jwt_utils import loader_user
        return loader_user(identity)

    @jwt_ext.invalid_token_loader
    @jwt_ext.unauthorized_loader
    def invalid_jwt_callback(error_string):
        return error(msg="无效的token", code=2040, http_code=401)

    @jwt_ext.expired_token_loader
    def expired_token_callback(jwt_headers, jwt_payload):
        return error(msg="token已过期", code=2040, http_code=401)

    @jwt_ext.user_lookup_error_loader
    def default_user_loader_error_callback(jwt_headers, jwt_payload):
        """
        """
        return error(msg="用户不存在", code=2040, http_code=401)
