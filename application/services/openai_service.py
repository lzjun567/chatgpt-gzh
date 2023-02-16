import logging

from application.extensions import openai_api, cache

logger = logging.getLogger(__name__)


def set_answer(openid, question):
    answer = openai_api.answer(question).strip()
    logger.info("获取answer:%s" % answer)
    cache.push(openid, answer)
