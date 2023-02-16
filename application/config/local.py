# -*- coding: utf-8 -*-
import os

from application.config.development import DevelopmentConfig



class LocalConfig(DevelopmentConfig):
    ENV = "local"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_ECHO = False   # 打印sql


