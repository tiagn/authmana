#!/usr/bin/python2
# -*- coding: utf8 -*-

from guard import auth
from guard import User
from guard import Role
from guard import Target


class EnglishModule(Target):
    pass


class ArticleModule(Target):
    pass


class EatModule(Target):
    pass


class person(User):

    @auth
    def read(self, obj):
        print('read: ', str(obj))

    @auth
    def update(self, obj):
        print('update', str(obj))

    @auth
    def delete(self, obj):
        print('delete', str(obj))

    @auth
    def create(self, obj):
        print('create', str(obj))


editor = Role()
editor.add_oper('read')
editor.add_oper('update')
editor.add_oper('delete')


reader = Role()
reader.add_oper('read')
reader.add_oper('update')

guest = Role()
guest.add_oper('read')

person1 = person()
person1.add_role(editor)

person2 = person()
person2.add_role(reader)

person3 = person()
person3.add_role(guest)

mod = EnglishModule()
mod.add_role(editor)
mod.add_role(reader)
mod.add_role(guest)

art = ArticleModule(mod)
art.add_role(editor)
art.add_role(reader)
art.add_role(guest)

eat = EatModule(art)


print(person1.can_or_not('read', mod), person2.can_or_not('read', mod), person3.can_or_not('read', mod))

print(person1.can_or_not('read', art), person2.can_or_not('read', art), person3.can_or_not('read', art))

print(person1.can_or_not('read', eat), person2.can_or_not('read', eat), person3.can_or_not('read', eat))

print(person1.can_or_not('update', mod), person2.can_or_not('update', mod), person3.can_or_not('update', mod))

print(person1.can_or_not('update', art), person2.can_or_not('update', art), person3.can_or_not('update', art))

print(person1.can_or_not('update', eat), person2.can_or_not('update', eat), person3.can_or_not('update', eat))

print(person1.can_or_not('delete', mod), person2.can_or_not('delete', mod), person3.can_or_not('delete', mod))

print(person1.can_or_not('delete', art), person2.can_or_not('delete', art), person3.can_or_not('delete', art))

print(person1.can_or_not('delete', eat), person2.can_or_not('delete', eat), person3.can_or_not('delete', eat))

print(person1.can_or_not('asdf', mod), person2.can_or_not('asdf', mod), person3.can_or_not('asdf', mod))

print(person1.can_or_not('asdf', art), person2.can_or_not('asdf', art), person3.can_or_not('asdf', art))

print(person1.can_or_not('asdf', eat), person2.can_or_not('asdf', eat), person3.can_or_not('asdf', eat))

# class user(User):
#
#     @auth
#     def read(self, obj):
#         print('read')
#
#     @auth
#     def create(self, obj):
#         print('create')
#
#     @auth
#     def aaa(self, obj):
#         print('aaa')
#
#     @auth
#     def destroy(self, obj):
#         print('destroy')
#
#     @auth
#     def update(self, obj):
#         print('update')
#
#
# class article(Target):
#     pass
#
#
# admin_role = Role()
# admin_role.add_oper('read')
# admin_role.add_oper('create')
# admin_role.add_oper('aaa')
# admin_role.add_oper('destroy')
# admin = user()
# admin.add_role(admin_role)
#
# art = article()
#
# print(admin.can_or_not('read', art))
# print(admin.can_or_not('create', art))
# print(admin.can_or_not('aaa', art))
# print(admin.can_or_not('destroy', art))
#
# user_role = Role()
# user_role.add_oper('read')
# user_role.add_oper('create')
# user_role.add_oper('aaa')
#
# user1 = user()
# user1.add_role(user_role)
#
# user_role2 = Role()
# user_role2.add_oper('read')
# user_role2.add_oper('create')
# user_role2.add_oper('aaa')
# # user_role2.add_oper('update')
#
# user2 = user()
# user2.add_role(user_role2)
# user1.add_role(user_role2)
#
# art2 = article()
#
# print(user2.can_or_not('read', art2))
# print(user2.can_or_not('create', art2))
# print(user2.can_or_not('aaa', art2))
# print(user2.can_or_not('update', art2))
# print(user1.can_or_not('update', art2))
#
# user1.create(art2)
# user2.update(art2)


# class module(Target):
#
#     def __init__(self, parent=None):
#         super(module, self).__init__(parent)
#
#
# class article(Target):
#
#     def __init__(self, parent=None):
#         super(article, self).__init__(parent)
#
#
# class person(User):
#
#
#     @auth
#     def create(self, obj: Target):
#         print('create')
#
#     @auth
#     def read(self, obj: Target):
#         print('read')
#
#     @auth
#     def delete(self, obj: Target):
#         print('delete')
#
#
# manager_role = Role()
# manager_role.add_oper('create')
# manager_role.add_oper('read')
# manager_role.add_oper('delete')
#
# employee_role = Role()
# employee_role.add_oper("read")
#
# employee2_role = Role()
# employee2_role.add_oper("read")
#
# user1 = person()
# user1.add_role(manager_role)
#
# user2 = person()
# user2.add_role(employee_role)
#
# user3 = person()
# user3.add_role(employee2_role)
#
# mod = module()
# mod.add_role(manager_role)
# mod.add_role(employee2_role)
# print(user1.can_or_not('create', mod))  # True
# print(user2.can_or_not('create', mod))  # False
#
# print(user1.can_or_not('read', mod))  # True
# print(user2.can_or_not('read', mod))  # True
#
# user1.create(mod)  # normal
# try:
#     user2.create(mod)  # raise Exception
# except PermissionError:
#     pass
#
# art = article(parent=mod)
#
# print(user1.can_or_not('create', art))  # True
# print(user2.can_or_not('create', art)  )# False
# print(user3.can_or_not('create', art) ) # False
#
# print(user1.can_or_not('read', art)  )# True
# print(user2.can_or_not('read', art) ) # False
# print(user3.can_or_not('read', art))  # True
#
# user1.create(art)  # return
# try:
#     user2.read(art)  # raise Exception
# except:
#     pass
# try:
#     user3.read(art)  # raise Exception
# except:
#     pass
