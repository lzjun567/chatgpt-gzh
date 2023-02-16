# -*- coding: utf-8 -*-
import os

from application.config.default import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database
    ENV = "testing"
