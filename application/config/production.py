# -*- coding: utf-8 -*-
import os
import urllib.parse

from .default import BaseConfig

class ProductionConfig(BaseConfig):
    ENV = "production"
    LOG_LEVEL = "INFO"
    SQLALCHEMY_ECHO = False

