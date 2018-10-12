# authmana -- 权限管理库

基于 用户-角色(权限)-目标 的权限管理库，可以管理比较复杂的权限， 只支持python3

# 说明
```
用户 -- 角色1（权限
     -- 角色2（权限

资源 -- 角色1（权限
 |   -- 角色2（权限
 下属
 |
资源2 -- 角色1（权限
```
用户对象和目标对象需要继承相应的类，角色对象直接实例化； 
 
每个用户和目标都需要分配相应的角色，角色可以管理权限； 
  
用户和目标需要拥有同一个角色才能验证角色是否有相关权限，否则无权；  

角色需要拥有相关的权限，否则无权；  

在编写用户类时在相关操作上需要设置 authman.auth 装饰器才能鉴权。

# 示例：
```
In [17]: import authmana

In [18]: role = authmana.Role()

In [19]: role.add_oper("read")

In [20]: class people(authmana.User):
    ...:
    ...:     @authmana.auth
    ...:     def read(self, target):
    ...:         print("read", target)
    ...:

In [21]: class item(authmana.Target):
    ...:     pass
    ...:
    ...:

In [22]: p = people()

In [23]: i = item()

In [24]: i.add_role(role)

In [26]: p.can_or_not('read', i)
Out[26]: False

In [27]: p.add_role(role)

In [28]: p.can_or_not('read', i)
Out[28]: True

In [29]: p.read(i)
read <__main__.item object at 0x000001C81F701668>
```

高级用法详见 test.py
