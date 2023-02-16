# -*- coding: utf-8 -*-

from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig
from .local import LocalConfig
from .default import BaseConfig

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'local': LocalConfig
}
