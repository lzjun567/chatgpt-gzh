"""
命令行工具
"""
import logging
import random
from typing import List

import click
from flask import current_app
from application.enum_field import MaterialType

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


def configure_cli(app):


    @app.cli.command("chat")
    @click.option("--question", prompt="问题")
    def chat_ai(question):
        """
        同步机构用户到营销平台
        """
        from application.extensions import openai_api
        answer = openai_api.answer(question)
        print(answer)

