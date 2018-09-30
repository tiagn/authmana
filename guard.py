#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
#
# @File Name: core.py
# @Desc:
# @Site:
# @Author:    yecj
# @date:      2018/9/27
# @Contact:   yecj@gzhhit.com

import uuid

from typing import List, Any
from functools import wraps


def auth(func):
    """验证"""

    @wraps(func)
    def wapper(who: User, what: Target, check: bool = False):
        user_roles = who.get_roles()
        work_roles = []
        # 获取可用的 role
        for role in user_roles:
            parent_roles = what.get_parent_roles()
            if OriginalTarget in parent_roles:
                work_roles.append(role)
            elif role in parent_roles:
                work_roles.append(role)
        if not work_roles:
            if check:
                return False
            raise PermissionError
        # role 是否有权限
        for role in work_roles:
            if role.can_or_not(func.__name__):
                break
        else:
            if check:
                return False
            raise PermissionError
        # 是否拒绝操作
        for role in work_roles:
            if role.deny_or_not(func.__name__):
                if check:
                    return False
                raise PermissionError
        if check:
            return True
        return func(who, what)

    return wapper


GLOBAL_ROLES = {}


def get_global_roles(id_: str):
    """为保证唯一，模块保存了所有的 Role 对象，此函数可以通过 id_ 获取已存在 Role 对象"""
    return GLOBAL_ROLES[id_]


def get_role_anyway(id_: str = None, opers: List[str] = None, incremental: bool = True, force: bool = False):
    """强制获取 Role 对象

    incremental: 增量增加 Role 对象的操作
    force: 强制更正 Role 对象的操作集
    """
    try:
        return Role(id_=id_, opers=opers)
    except KeyError:
        role = get_global_roles(id_)
        if opers:
            if incremental:
                for oper in opers:
                    role.add_oper(oper)
            if force:
                for oper in role.get_opers():
                    role.del_oper(oper)
                for oper in opers:
                    role.add_oper(oper)
        return role


class Role:
    """角色类 -- how

    角色类是权限的集合，通过 add_oper 增加操作，代表允许的操作

    通过 _opers 和 _id 参数来标识一个唯一的角色对象

    如果需要序列化保存，需要序列化 Role 的 _opers 和 _id 参数
    """

    def __init__(self, id_: str = None, opers: List[str] = None, deny_opers: List[str] = None):
        self._opers = opers if opers else []
        self._deny_opers = deny_opers if deny_opers else []
        self._id = id_ if id_ else uuid.uuid4().hex
        global GLOBAL_ROLES
        if self._id in GLOBAL_ROLES:
            raise KeyError(f'[{id}] Role instance already exist, please get it from guard.get_global_roles(id_)')
        GLOBAL_ROLES[self._id] = self

    def get_id(self):
        """获取对象 id"""
        return self._id

    def __eq__(self, other):
        if hasattr(other, '_id') and hasattr(other, '_opers'):
            return self._id == other._id and set(self._opers) == set(other._opers)
        return False

    def add_oper(self, oper: str):
        """增加操作"""
        if not isinstance(oper, str):
            raise TypeError
        if oper not in self._opers:
            self._opers.append(oper)

    def del_oper(self, oper: str):
        """删除操作"""
        if not isinstance(oper, str):
            raise TypeError
        if oper in self._opers:
            self._opers.remove(oper)

    def get_opers(self):
        """获取操作集"""
        return self._opers

    def can_or_not(self, oper: str):
        """是否可以"""
        if not isinstance(oper, str):
            raise TypeError
        if oper in self._opers:
            return True
        else:
            return False

    def deny_oper(self, oper: str):
        """拒绝操作"""
        if not isinstance(oper, str):
            raise TypeError
        if oper not in self._deny_opers:
            self._deny_opers.append(oper)

    def remove_deny_oper(self, oper: str):
        """拒绝操作"""
        if not isinstance(oper, str):
            raise TypeError
        if oper in self._deny_opers:
            self._deny_opers.remove(oper)

    def get_deny_opers(self):
        """获取拒绝操作集"""
        return self._deny_opers

    def deny_or_not(self, oper: str):
        """是否拒绝"""
        if not isinstance(oper, str):
            raise TypeError
        if oper in self._deny_opers:
            return True
        else:
            return False


class OriginalTarget:
    """原始 Target

    所有没有明确 _parent 的 Target 的 _parent 都是本类对象
    id_ 为 True，表示此 Target 为 OriginalTarget
    """

    def __init__(self, id_: bool = True):
        self._id = id_ if id_ else uuid.uuid4().hex

    def get_id(self):
        return self._id

    def get_roles(self):
        return [OriginalTarget]


class RoleOper:
    """角色操作类

    抽象出来用于对 Role 对象进行操作的类
    """

    def __init__(self, id_: str = None, roles: List[Role] = None):
        self._id = id_ if id_ else uuid.uuid4().hex
        self._roles = roles if roles else []

    def get_id(self):
        """获取对象 id_"""
        return self._id

    def add_role(self, role: Any):
        """添加 role"""
        if not isinstance(role, Role):
            raise TypeError
        if role not in self._roles:
            self._roles.append(role)

    def del_role(self, role: Role):
        """删除 role"""
        if not isinstance(role, Role):
            raise TypeError
        if role in self._roles:
            self._roles.remove(role)

    def get_roles(self):
        """获取 roles"""
        return self._roles


class Target(RoleOper):
    """目标类 -- what

    用户对象需要操作的目标都需要继承此类
    Target 对象需要通过 Role 对象来表示 Target 对象所拥有的权限

    如果 _parent 为 True，则说明 Target 是根 Target， 根 Target 的 _parent 为 OriginalTarget 对象
    通过 _id 和 _roles 和 _parent 参数来标识一个唯一的目标对象

    如果需要序列化保存，需要序列化 Role 的 _id， _opers 和 _parent 参数
    """

    def __init__(self, parent=None, id_: str = None, roles: List[Role] = None):
        super(Target, self).__init__(id_=id_, roles=roles)
        self._parent = parent if parent else OriginalTarget()

    def get_parent(self):
        """获取上一级 Target"""
        return self._parent

    def get_parent_id(self):
        """获取上一级 Target 的 id"""
        return self._parent.get_id()

    def get_parent_roles(self):
        """获取上一级 Target 的 role"""
        return self._parent.get_roles()


class InheritTarget(Target):
    """继承目标类

    需要继承 parent 的 roles 的类
    其他同 Target

    """

    def __init__(self, parent=None, id_: str = None, roles: List[Role] = None):
        super(InheritTarget, self).__init__(id_=id_, roles=roles, parent=parent)
        for role in self.get_parent_roles():
            self.add_role(role)


class User(RoleOper):
    """用户类 -- who

    账号、用户之类的需要权限限制的主体都需要继承此类
    User 对象需要通过 Role 对象来表示 User 对象所拥有的权限

    通过 _id 和 _roles 参数来标识一个唯一的用户对象

    如果需要序列化保存，需要保存 User 的 _id 和 _roles 参数
    """

    def __init__(self, id_: str = None, roles: List[Role] = None):
        super(User, self).__init__(id_=id_, roles=roles)

    def can_or_not(self, oper: str, target: Target):
        """是否可以操作 Target"""
        if not isinstance(oper, str) or not isinstance(target, Target):
            raise TypeError
        oper = getattr(self, oper, None)
        if not oper:
            return False
        return auth(oper)(self, target, check=True)
