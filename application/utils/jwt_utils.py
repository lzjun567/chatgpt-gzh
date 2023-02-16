from functools import wraps

from flask import current_app, request
from flask_jwt_extended import (
    verify_jwt_in_request, create_access_token, get_current_user,
    get_jwt_identity, create_refresh_token
)

from application.errors import AuthorizationError
from application.errors import LoginInAnotherDeviceError, AuthDeleteError, AuthForbiddenError
from application.extensions import authapi
from application.models.user import InstitutionUser, StudentUser, Staff, User


def create_jwt_token(user, expires_delta=None, platform=None):
    """创建jwt token"""
    return _create_token("access_token", user, expires_delta=expires_delta, platform=platform)


def create_jwt_refresh_token(user, expires_delta=None, platform=None):
    """创建jwt refresh token"""
    return _create_token("refresh_token", user, expires_delta=expires_delta, platform=platform)


def _create_token(token_type, user, expires_delta=None, platform=None):
    if isinstance(user, InstitutionUser):
        identity = {'type': 'institution', 'id': user.id, 'platform': platform}
    elif isinstance(user, StudentUser):
        identity = {'type': 'student', 'id': user.id, 'platform': platform}
    elif isinstance(user, Staff):
        identity = {'type': 'staff', 'id': user.id, 'platform': platform}
    elif isinstance(user, User):
        # 此时的user是没有关联机构的的，上面的都是关联了具体的机构的token
        identity = {'type': 'user', 'id': user.id, 'platform': platform}
    else:
        raise ValueError("Invalid user type")
    if token_type == 'access_token':
        return create_access_token(identity, expires_delta=expires_delta)
    else:
        return create_refresh_token(identity, expires_delta=expires_delta)


def login_required(user_type):
    """检查是否登录"""

    def login_wrapper(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity() or {}

            if user_type and identity.get('type') != user_type:
                raise AuthorizationError(msg="非法用户类型")
            else:
                return fn(*args, **kwargs)

        return wrapper

    return login_wrapper


# 校验jwt是否是合法的机构用户
# institution_user_required = login_required('institution')

institution_user_required2 = authapi.user_required(role='institution')
institution_user_required = institution_user_required2
# 校验jwt是否是合法的学员
student_user_required = login_required('student')
# 校验jwt是否是合法的员工
staff_user_required = authapi.user_required(role='staff')
# 账号登录
user_required = login_required('user')  # 还没关联机构的登录
# 不限制用户类型，任意用户类型
any_user_required = login_required(None)


def loader_user(identity):
    """通过jwt identity获取用户"""
    user_type = identity.get('type')
    user_id = identity.get('id')
    platform = identity.get('platform')
    if user_type == 'institution':
        institution_user = InstitutionUser.query.get(user_id)
        if not institution_user:
            return institution_user
        if institution_user.is_deleted:
            raise AuthDeleteError("您的帐号暂无权限，请联系管理员~")
        if not institution_user.is_enabled:
            raise AuthForbiddenError("您的帐号暂无权限，请联系管理员~")
        institution_user.check_roles()
        return institution_user
    if user_type == 'user':
        user = User.query.get(user_id)
        return user
    if user_type == 'student':
        student_user = StudentUser.query.get(user_id)
        if not student_user:
            return None
        if student_user.is_deleted:
            raise AuthDeleteError("您的帐号暂无权限，请联系管理员~")
        if not student_user.is_enabled:
            raise AuthForbiddenError("您的帐号暂无权限，请联系管理员~")
        auth_header = request.headers.get(current_app.config.get('JWT_HEADER_NAME'), "").replace("Bearer ", "")
        if "/refresh" not in request.path:
            # refresh 接口使用的refresh_token，不做判断
            # h5 平台 和 pc平台要求各自登录互踢
            if platform == 'h5' and auth_header != student_user.h5_token:
                raise LoginInAnotherDeviceError(
                    error_info=f"platform:{platform} \nrequest_token:{auth_header}\n token:{student_user.h5_token}")
            if platform == 'pc' and auth_header != student_user.pc_token:
                raise LoginInAnotherDeviceError(
                    error_info=f"platform:{platform} \nrequest_token:{auth_header}\n token:{student_user.pc_token}")
        return student_user
    elif user_type == 'staff':
        return Staff.query.get(user_id)
    else:
        return None


def get_institution_user() -> InstitutionUser:
    """获取当前登录的机构用户"""
    # return get_current_user()
    return get_institution_user2()

def get_institution_user2() -> InstitutionUser:
    """获取当前登录的机构用户"""
    from application.contrib.authapi import get_current_user
    return get_current_user()


def get_staff_user() -> Staff:
    """获取当前登录的内部员工"""
    # return get_current_user()
    from application.contrib.authapi import get_current_user
    return get_current_user()


def get_student_user() -> StudentUser:
    """获取当前登录的内部员工"""
    return get_current_user()
