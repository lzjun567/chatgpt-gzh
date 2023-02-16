# -*- coding:utf-8 -*-
from functools import wraps
from typing import List

from application.errors import PermissionDeniedError
from application.utils.jwt_utils import get_institution_user


def permission(allowed_permission_code: str = None, allowed_role_code: List[str] = None):
    """
    用户权限判断
    :param allowed_role_code 可以操作的角色code码列表
    :param allowed_permission_code 某个操作所需要的权限code码
    """

    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not allowed_role_code and not allowed_permission_code:
                return func(*args, **kwargs)
            current_user = get_institution_user()

            # 超级管理员和创建者拥有所有权限
            if 'super' in current_user.role_codes or 'creator' in current_user.role_codes:
                return func(*args, **kwargs)

            # 如果用户角色列表中没有指定的角色code，提示无权限
            if allowed_role_code and not (set(current_user.role_codes) & set(allowed_role_code)):
                raise PermissionDeniedError()

            if allowed_permission_code not in current_user.permissions:
                raise PermissionDeniedError()
            return func(*args, **kwargs)

        return wrapper

    return decorators
