ERROR_CODE = {

    200: "success",
}
class ApiError(Exception):
    """所有服务异常的基类"""
    code = 500
    http_code = 400
    data = None
    error_info = ""
    msg = ""

    def __init__(self, msg=None, code=None, data=None, error_info=None, http_code=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code

        if data:
            self.data = data

        if http_code:
            self.http_code = http_code

        self.error_info = error_info


class RequestDataError(ApiError):
    code = 1002
    http_code = 400
    msg = "请求参数错误"


class AuthForbiddenError(ApiError):
    """鉴权失败异常 用户已禁用"""
    code = 2042
    http_code = 401
    msg = "您的帐号暂无权限，请联系管理员~"


class MaterialError(ApiError):
    code = 6200
    http_code = 400


class UserProfileError(ApiError):
    code = 6400
    http_code = 400


class WechatError(ApiError):
    code = 6500
    http_code = 400


class WxTemplateError(ApiError):
    code = 6600
    http_code = 400
