# guard -- 权限管理库

项目
    模块1
        任务1
            讨论
        任务2
    模块2
        任务1
管理人  增删改查
参与人
游客  特定模块
    查

用户 -- 角色1（权限
     -- 角色2（权限

资源 -- 角色1（权限
 |    -- 角色2（权限
 下属
 |
资源 -- 角色1（权限


import guard
guard.GLOBAL_ROLES
from guard import Role
a = Role()