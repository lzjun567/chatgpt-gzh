# -*- coding: utf-8 -*-
import json
import logging
import unittest

from flask import current_app

from application import create_app
from application.contants import DEFAULT_ERROR_CODE
from application.enum_field import CourseKind
from application.utils.random_utils import random_str
from .base.http import HTTPBaseTestCase


class BaseTestCase(HTTPBaseTestCase):

    def create_app(self):
        app = create_app("testing")
        logger = logging.getLogger()
        logger.setLevel(level=logging.INFO)
        return app

    def setUp(self):
        """创建所有表"""

        pass

    def tearDown(self):
        """清空session并删除所有表"""
        pass





if __name__ == '__main__':
    unittest.main()
