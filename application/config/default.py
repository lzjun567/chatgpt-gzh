# -*- coding: utf-8 -*-

import urllib.parse
import os


class BaseConfig:
    PROJECT = "api"
    PROFILE = True
    ENV = "development"
    PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DEBUG = True
    SECRET_KEY = ''

    WECHAT_APPID = os.getenv("WECHAT_APPID")
    WECHAT_SECRET = os.getenv("WECHAT_SECRET")
    WECHAT_SESSION_PREFIX = 'wechat_'
    WECHAT_TOKEN = 'wx123'
    WECHAT_TYPE = 0
    WECHAT_TIMEOUT = 1
    WECHAT_AUTO_RETRY = True

    OPENAI_KEY = os.getenv("OPENAI_KEY")

    REDIS_PASSWORD = urllib.parse.quote(os.getenv("REDIS_PWD") or "")
    REDIS_URL = 'redis://:%s@127.0.0.1:6379' % REDIS_PASSWORD
