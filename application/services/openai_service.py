import logging

from application.extensions import openai_api, cache

logger = logging.getLogger(__name__)

CHATDATA = {}  # 保存历史记录


def set_answer(openid, question):
    answer = openai_api.answer(question, context=CHATDATA.get(openid)).strip()
    CHATDATA.setdefault(openid, []).append({"role": "user", "content": question})
    CHATDATA[openid].append({"role": "assistant", "content": answer})
    CHATDATA[openid] = CHATDATA[openid][-8:]
    logger.info("获取answer:%s" % answer)
    cache.push(openid, answer)
