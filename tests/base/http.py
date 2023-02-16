# -*- coding: utf-8 -*-
import datetime
import json
import urllib.parse

from flask_testing import TestCase


class HTTPBaseTestCase(TestCase):

    def post(self, url, headers={}, auth_user=None, refresh_token=False, **kwargs):
        """
        POST 请求API， 会加上认证信息
        """
        if auth_user:
            headers['Authorization'] = "Bearer " + (create_jwt_token(
                auth_user) if not refresh_token else create_jwt_refresh_token(auth_user))
        response = self.client.post(url, headers=headers, **kwargs)
        return response

    def put(self, url, headers={}, auth_user=None, **kwargs):
        """
        PUT请求API， 会加上认证信息
        """
        if auth_user:
            headers['Authorization'] = "Bearer " + create_jwt_token(auth_user)

        response = self.client.put(url, headers=headers, **kwargs)
        return response

    def get(self, url, headers=None, auth_user=None, params=None, **kwargs):
        """
        GET请求API， 会加上认证信息
        """
        if not headers:
            headers = dict()

        def format_value(value):
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            if isinstance(value, bool):
                if value:
                    return 1
                else:
                    return 0

            return value

        if params:
            params = {k: format_value(v) for k, v in params.items()}
            s = urllib.parse.urlencode(params, doseq=True)  # 支持数组解析
            url = url + "?" + s

        if auth_user:
            headers['Authorization'] = "Bearer " + create_jwt_token(auth_user)

        response = self.client.get(url, headers=headers, **kwargs)
        return response

    def delete(self, url, headers={}, auth_user=None, **kwargs):
        """
        DELETE请求API， 会加上认证信息
        """
        if auth_user:
            headers['Authorization'] = "Bearer " + create_jwt_token(auth_user)

        response = self.client.delete(url, headers=headers, **kwargs)
        db.session.expire_all()
        return response

    def assertSuccess(self, response):
        """
        检查是否返回成功
        """

        self.assert200(response)
        self.assertEqual(response.json['code'], 200)

    def assertError(self, response, code):
        """
        检查返是否返回正确参数错误返回值
        """
        print(response.json)
        self.assertEqual(response.json['code'], code)
        self.assertEqual(response.json['status'], 'error')

    def json(self, response):
        data = json.loads(response.data)
        return json.dumps(data)

    def pprint_response(self, response):
        import pprint
        pprint.pprint(json.loads(response.data))

    def data(self, response):
        return json.loads(response.data).get("data")
