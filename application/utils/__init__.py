import hashlib
import hmac
import logging
import re
from datetime import datetime

from flask import current_app, Request

from .random_utils import random_num_str, random_str, random_order_number, random_base16_num_str
from .response_utils import error
from .response_utils import success
from .time_utils import timestamp_to_datetime

logger = logging.getLogger(__name__)

def make_hmac(key, data):
    """
    HMAC-SHA256签名算法
    """

    if isinstance(key, str):
        key = bytes(key, encoding="utf-8")
    if isinstance(data, str):
        data = bytes(data, encoding="utf-8")
    hash = hmac.new(key, data, digestmod=hashlib.sha256)
    result = hash.digest()
    return result


# 用来做表单数据自动转换用的函数
coerceDate = lambda d: datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f")


def make_md5(data):
    md = hashlib.md5()
    md.update(data.encode("utf-8"))
    result = md.hexdigest()
    return result


def sub_dict(d: dict, included_keys: list):
    return {k: d[k] for k in included_keys if k in d}


def list_is_equals(a_list, b_list):
    """
    判断两个列表中是否含有相同的元素
    """
    return set(a_list) == set(b_list)


def get_institution_code_by_hostname(host: str):
    """
    从host中提取出机构code
    :param host: xinylzb40765841-h5.youbaokeji.cn
    """
    match = re.search(r"(live|xinylzb)(\w*)-h5\.*?", host)
    if match:
        institution_code = match.group(2)
    else:
        institution_code = current_app.config.get("DEFAULT_INSTITUTION_CODE")
    return institution_code


def get_institution_code_by_request(request: Request):
    """
    从request的请求头名叫hostx取出前端传的访问域名后解析出code
    :param host: xinylzb40765841-h5.youbaokeji.cn
    """
    hostx = request.headers.get("hostx")
    logger.info("hosts:%s", hostx)
    if not hostx:
        hostx = request.headers.get("referer")
        logger.info("referer:%s", hostx)
    return get_institution_code_by_hostname(hostx)



