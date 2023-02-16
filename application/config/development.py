# -*- coding: utf-8 -*-
import os
import urllib.parse

from .default import BaseConfig


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_ECHO = False  # 打印sql

    PROFILE = True
    SQLALCHEMY_RECORD_QUERIES = True
    DATABASE_QUERY_TIMEOUT = 0.5
