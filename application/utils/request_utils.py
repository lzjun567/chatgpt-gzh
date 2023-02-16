from typing import Type, Dict
import urllib.parse as urlparse
from pydantic import BaseModel
from werkzeug.datastructures import MultiDict


def convert_query_params(query_prams: MultiDict, model: Type[BaseModel]) -> dict:
    """
    :param query_prams: flask request.args
    :param model: query parameter's model
    :return resulting parameters
    """
    return {
        **query_prams.to_dict(),
        **{key: value for key, value in query_prams.to_dict(flat=False).items() if
           key in model.__fields__ and model.__fields__[key].is_complex()}
    }


def get_url_queries(url, *args) -> Dict:
    """
    提取URL中的查询参数
    :param url:
    :param args:  参数，可传多个
    :return:
    """
    parsed = urlparse.urlparse(url)
    queries = urlparse.parse_qs(parsed.query)
    return {k: v[0] for k, v in queries.items() if k in args}

def get_client_ip():
    from flask import request
    return request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('HTTP_X_REAL_IP') or request.environ.get(
        'REMOTE_ADDR')
