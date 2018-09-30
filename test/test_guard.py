#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
#
# @File Name: test_guard
# @Desc:
# @Site: 
# @Author:    yecj
# @date:      2018/9/29
# @Contact:   yecj@gzhhit.com
import pytest

from guard import Target, User, Role, auth, get_role_anyway


class EnglishModule(Target):
    pass


class ArticleModule(Target):
    pass


class EatModule(Target):
    pass


class person(User):

    @auth
    def read(self, obj):
        return 'read'

    @auth
    def update(self, obj):
        return 'update'

    @auth
    def delete(self, obj):
        return 'delete'

    @auth
    def create(self, obj):
        return 'create'


class TestGuard:
    # 创建 3 个角色， editor， writer， guest

    editor = Role()
    editor.add_oper('read')
    editor.add_oper('update')
    editor.add_oper('delete')
    editor.add_oper('create')

    writer = get_role_anyway()
    writer.add_oper('read')
    writer.add_oper('create')

    guest = get_role_anyway()
    guest.add_oper('read')

    # 准备父类 Target 对象，准备对应的角色，添加基础的操作 （权限）
    mod_read = get_role_anyway()
    mod_read.add_oper('read')

    mod = Target()
    mod.add_role(mod_read)
    mod.add_role(editor)

    # 创建 3 个对象 mod，art，eat 其中 mod 对象下属模块有 art 对象，art 对象下属模块是eat 对象
    eng = EnglishModule(parent=mod)
    eng.add_role(editor)
    eng.add_role(writer)
    eng.add_role(guest)

    art = ArticleModule(eng)
    art.add_role(editor)
    art.add_role(writer)

    eat = EatModule(art)

    # 创建 3 个用户 user1，user2，user3
    user1 = person()
    user1.add_role(mod_read)
    user1.add_role(editor)

    user2 = person()
    user2.add_role(mod_read)
    user2.add_role(writer)

    user3 = person()
    user3.add_role(mod_read)
    user3.add_role(guest)

    def test_read(self):
        oper = 'read'
        assert self.user1.can_or_not(oper, self.eng) is True
        assert self.user2.can_or_not(oper, self.eng) is True
        assert self.user3.can_or_not(oper, self.eng) is True

        assert self.user1.read(self.eng) == oper
        assert self.user2.read(self.eng) == oper
        assert self.user3.read(self.eng) == oper

        assert self.user1.can_or_not(oper, self.art) is True
        assert self.user2.can_or_not(oper, self.art) is True
        assert self.user3.can_or_not(oper, self.art) is True

        assert self.user1.read(self.art) == oper
        assert self.user2.read(self.art) == oper
        assert self.user3.read(self.art) == oper

        assert self.user1.can_or_not(oper, self.eat) is True
        assert self.user2.can_or_not(oper, self.eat) is True
        assert self.user3.can_or_not(oper, self.eat) is False

        assert self.user1.read(self.eat) == oper
        assert self.user2.read(self.eat) == oper
        with pytest.raises(PermissionError):
            assert self.user3.read(self.eat) == oper

    def test_create(self):
        oper = 'create'
        assert self.user1.can_or_not(oper, self.eng) is True
        assert self.user2.can_or_not(oper, self.eng) is False
        assert self.user3.can_or_not(oper, self.eng) is False

        assert self.user1.create(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user2.create(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user3.create(self.eng) == oper

        assert self.user1.can_or_not(oper, self.art) is True
        assert self.user2.can_or_not(oper, self.art) is True
        assert self.user3.can_or_not(oper, self.art) is False

        assert self.user1.create(self.art) == oper
        assert self.user2.create(self.art) == oper
        with pytest.raises(PermissionError):
            assert self.user3.create(self.art) == oper

        assert self.user1.can_or_not(oper, self.eat) is True
        assert self.user2.can_or_not(oper, self.eat) is True
        assert self.user3.can_or_not(oper, self.eat) is False

        assert self.user1.create(self.eat) == oper
        assert self.user2.create(self.eat) == oper
        with pytest.raises(PermissionError):
            assert self.user3.create(self.eat) == oper

    def test_delete(self):
        oper = 'delete'
        assert self.user1.can_or_not(oper, self.eng) is True
        assert self.user2.can_or_not(oper, self.eng) is False
        assert self.user3.can_or_not(oper, self.eng) is False

        assert self.user1.delete(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user2.delete(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user3.delete(self.eng) == oper

        assert self.user1.can_or_not(oper, self.art) is True
        assert self.user2.can_or_not(oper, self.art) is False
        assert self.user3.can_or_not(oper, self.art) is False

        assert self.user1.delete(self.art) == oper
        with pytest.raises(PermissionError):
            assert self.user2.delete(self.art) == oper
        with pytest.raises(PermissionError):
            assert self.user3.delete(self.art) == oper

        assert self.user1.can_or_not(oper, self.eat) is True
        assert self.user2.can_or_not(oper, self.eat) is False
        assert self.user3.can_or_not(oper, self.eat) is False

        assert self.user1.delete(self.eat) == oper
        with pytest.raises(PermissionError):
            assert self.user2.delete(self.eat) == oper
        with pytest.raises(PermissionError):
            assert self.user3.delete(self.eat) == oper

    def test_unknown_oper(self):
        oper = 'unknown'
        assert self.user1.can_or_not(oper, self.eng) is False
        assert self.user2.can_or_not(oper, self.eng) is False
        assert self.user3.can_or_not(oper, self.eng) is False

        assert self.user1.can_or_not(oper, self.art) is False
        assert self.user2.can_or_not(oper, self.art) is False
        assert self.user3.can_or_not(oper, self.art) is False

        assert self.user1.can_or_not(oper, self.eat) is False
        assert self.user2.can_or_not(oper, self.eat) is False
        assert self.user3.can_or_not(oper, self.eat) is False


class TestGuardBlack:
    """黑名单测试"""

    # 创建 3 个角色， editor， writer， guest
    editor = Role()
    editor.add_oper('read')
    editor.add_oper('update')
    editor.add_oper('delete')
    editor.add_oper('create')

    writer = get_role_anyway()
    writer.add_oper('read')
    writer.add_oper('create')

    black_write = get_role_anyway()
    black_write.deny_oper('create')

    # 准备父类 Target 对象，准备对应的角色，添加基础的操作 （权限）
    mod_read = get_role_anyway()
    mod_read.add_oper('read')

    mod = Target()
    mod.add_role(mod_read)
    mod.add_role(editor)

    # 创建 3 个对象 mod，art，eat 其中 mod 对象下属模块有 art 对象，art 对象下属模块是eat 对象
    eng = EnglishModule(parent=mod)
    eng.add_role(editor)
    eng.add_role(writer)
    eng.add_role(black_write)

    art = ArticleModule(eng)
    art.add_role(editor)
    art.add_role(writer)

    eat = EatModule(art)

    # 创建 3 个用户 user1，user2，user3
    user1 = person()
    user1.add_role(mod_read)
    user1.add_role(editor)

    user2 = person()
    user2.add_role(mod_read)
    user2.add_role(writer)

    user3 = person()
    user3.add_role(mod_read)
    user3.add_role(writer)
    user3.add_role(black_write)

    def test_create(self):
        oper = 'create'
        assert self.user1.can_or_not(oper, self.eng) is True
        assert self.user2.can_or_not(oper, self.eng) is False
        assert self.user3.can_or_not(oper, self.eng) is False

        assert self.user1.create(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user2.create(self.eng) == oper
        with pytest.raises(PermissionError):
            assert self.user3.create(self.eng) == oper

        assert self.user1.can_or_not(oper, self.art) is True
        assert self.user2.can_or_not(oper, self.art) is True
        assert self.user3.can_or_not(oper, self.art) is False

        assert self.user1.create(self.art) == oper
        assert self.user2.create(self.art) == oper
        with pytest.raises(PermissionError):
            assert self.user3.create(self.art) == oper

        assert self.user1.can_or_not(oper, self.eat) is True
        assert self.user2.can_or_not(oper, self.eat) is True
        assert self.user3.can_or_not(oper, self.eat) is True

        assert self.user1.create(self.eat) == oper
        assert self.user2.create(self.eat) == oper
        assert self.user3.create(self.eat) == oper
