# -*- coding: utf-8 -*-

from collections import namedtuple

# 默认问题码， 未知异常
DEFAULT_ERROR_CODE = 500

# 默认角色
DEFAULT_INSTITUTION_ROLES = [
    ('高级管理员', 'senior_admin'),
    ('普通管理员', 'normal_admin'),
]

# 通用验证码
UNIVERSAL_VERIFY_CODE = '0000'

# 学习状态
STUDY_STATUS = namedtuple("StudyStatus", "no_start, learning, finish, end")(0, 1, 2, 3)

HTTP_STATUS_CODES = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",  # see RFC 8297
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi Status",
    208: "Already Reported",  # see RFC 5842
    226: "IM Used",  # see RFC 3229
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",  # unused
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",  # unused
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",  # see RFC 2324
    421: "Misdirected Request",  # see RFC 7540
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",  # see RFC 8470
    426: "Upgrade Required",
    428: "Precondition Required",  # see RFC 6585
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    449: "Retry With",  # proprietary MS extension
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",  # see RFC 2295
    507: "Insufficient Storage",
    508: "Loop Detected",  # see RFC 5842
    510: "Not Extended",
    511: "Network Authentication Failed",  # see RFC 6585
}

# wsapp 的回调消息状态码
WSAPI_CALLBACK_STATUS_CODE = {
    100: "replaced登录",
    101: "链接已断开!",
    200: "登录成功",
    202: "已在线",
    -401: "密钥认证失败",
    403: "当前账号被禁止使用",

    2000: "对话消息=2000",  # 接收到消息
    2001: "已送达消息返回xml",
    2004: "presence回调消息返回xml",
    2005: "对方和自己已读消息回执返回xml",

}
