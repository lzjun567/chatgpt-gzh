import logging
import time

from application.extensions import openai_api, cache

logger = logging.getLogger(__name__)

CHAT_DATA = dict()  # 保存历史记录


def set_answer(openid, question):
    logger.info("获取question:%s" % question)
    answer = openai_api.answer(question, context=CHAT_DATA.get(openid)).strip()
    CHAT_DATA.setdefault(openid, []).append({"role": "user", "content": question, 't': time.time()})
    CHAT_DATA[openid].append({"role": "assistant", "content": answer, 't': time.time()})
    CHAT_DATA[openid] = CHAT_DATA[openid][-5:]
    logger.info("获取answer:%s" % answer)
    cache.push(openid, answer)
