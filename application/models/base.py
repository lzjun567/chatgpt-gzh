# -*- coding: utf-8 -*-
import json
from datetime import datetime

import inflection
from sqlalchemy import Column, Boolean
from sqlalchemy.ext import mutable
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import ClauseElement

from application.extensions import db
from application.utils import random_utils


class DatetimeMixin:
    __abstract__ = True
    """创建时间和修改时间mixin， 参考
    """
    id = db.Column(db.String(24), primary_key=True, comment="主键", name='id', default=random_utils.objectid)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="最后更新时间")
    deleted_at = db.Column(db.DateTime, comment='删除时间', nullable=True)


class JsonArray(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    @property
    def python_type(self):
        return list

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        else:
            return json.loads(value)


mutable.MutableList.associate_with(JsonArray)


class JsonDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    @property
    def python_type(self):
        return dict

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonDict)


class BaseModel(DatetimeMixin, db.Model):
    """
    :type: sqlalchemy.orm.Session
    """
    is_enable = Column(Boolean, default=True, nullable=False, comment="是否可用")
    is_deleted = Column(Boolean, default=False, comment="是否已删除")  # 原来的用户状态:'-1删除,0禁用,1启用
    __abstract__ = True

    default_fields = []

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    @declared_attr
    def __tablename__(cls):
        return inflection.underscore(cls.__name__)

    def update(self, **kwargs):
        keys = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
        return self

    def can_edit_visible(self, user, category) -> bool:
        """
        判断user是否可以编辑
        只有创建者、超级管理员、机构创建者才有编辑权限
        :param user:  InstitutionUser
        :param category ResourceCategory
        :return: bool
        """
        result = any([user.id == self.created_by_id, 'creator' in user.role_codes])
        return result

    def to_dict(self, show=None, hide=None, path=None, show_all=None, list_item=False):
        """ Return a dictionary representation of this model.
        """

        if not show:
            show = []
        if not hide:
            hide = []
        hidden = []
        if hasattr(self, 'hidden_fields'):
            hidden = self.hidden_fields
        default = []
        if hasattr(self, 'default_fields'):
            default = self.default_fields
            if self.default_fields == 'all' and not show:
                default = self.__table__.columns.keys() \
                          + self.__table__.columns.keys() \
                          + dir(self)
        ret_data = {}

        if not path:
            path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split('.', 1)[0] == path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != '.':
                    item = '.%s' % item
                item = '%s%s' % (path, item)
                return item

            show[:] = [prepend_path(x) for x in show]
            hide[:] = [prepend_path(x) for x in hide]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        for key in columns:
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                if not list_item:
                    hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    ret_data[key] = []
                    for item in getattr(self, key):
                        ret_data[key].append(item.to_dict(
                            show=[],
                            hide=hide,
                            path=('%s.%s' % (path, key.lower())),
                            show_all=show_all,
                            list_item=True
                        ))
                else:
                    if self.__mapper__.relationships[key].query_class is not None:
                        if getattr(self, key):
                            ret_data[key] = getattr(self, key).to_dict(
                                show=[],
                                hide=hide,
                                path=('%s.%s' % (path, key.lower())),
                                show_all=show_all,
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            check = '%s.%s' % (path, key)
            if check in hide or key in hidden:
                continue

            if show_all or check in show or key in default:
                val = getattr(self, key)
                # 过滤掉非property的方法
                if not isinstance(getattr(type(self), key), property):
                    continue

                if callable(val):
                    val = val()
                try:
                    ret_data[key] = val
                except:
                    pass

        return ret_data

    @classmethod
    def order_fields(cls, order_bys: str):
        """
        排序处理
        param:order_bys, 用逗号分隔的排序字段， 字段如果以“-”开头则为升序
        """
        if not order_bys:
            return
        order_bys = order_bys.split(",")
        orders = []
        for i in order_bys:
            field = i[1:] if i.startswith("-") else i
            if hasattr(cls, field):
                if i.startswith("-"):
                    orders.append(getattr(cls, field))
                else:
                    # 降序
                    orders.append(getattr(cls, field).desc())
        return orders

    @classmethod
    def build_query(cls, query: Query = None, **kwargs):
        """
        根据指定参数构建过滤条件
        """
        if query is None:
            query = cls.query.filter_by(**kwargs)
        else:
            query = query.filter_by(**kwargs)
        return query

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        instance = cls.query.filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = cls(**params)
            db.session.add(instance)
            db.session.flush()
            return instance, True

    @classmethod
    def upsert(cls, filter_data: dict, update_data: dict):
        """
        插入或更新
        """
        instance = cls.query.filter_by(**filter_data).first()
        if not instance:
            instance = cls(**filter_data)
        instance.update(**update_data)
        db.session.add(instance)
        return instance

    @classmethod
    def get_by_id(cls, _id: str):
        return cls.query.get(_id)


class CategoryModel(BaseModel):
    """
    分类基类
    """
    __abstract__ = True
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, default=0, nullable=True)
    key = db.Column(db.String(100), default="")  # 第0层 直接用“”表示，第一层用“主键id-”表示
    position = db.Column(db.Integer, default=0)  # 同层级的子节点的先后顺序
    is_deleted = db.Column(db.Boolean, nullable=True, default=False, comment="是否删除")

    @declared_attr
    def institution_id(cls):
        return db.Column(db.String(24), db.ForeignKey('institution.id', use_alter=True), comment="机构id")

    @declared_attr
    def created_by_id(cls):
        return db.Column(db.String(24), db.ForeignKey('institution_user.id'), comment="创建这个课程的员工", nullable=True)

    default_fields = ['id', 'name', "description", "created_at"]
