# opstool
## django restful 项目

写个这个项目主要是为了练手，总是 crud，写个能直接上手的业务框架，能开箱即用，方便后续开发。

做这个项目的想法思路是感觉自己到了一个瓶颈，不能安静下来看书，学习的一些知识点也不够牢固。
也把平时挖的坑填上，但自己的业务代码都不想改，也没有单测，想想还是新挖一个坑比较方便。

把自己遇到的常用业务功能加上，这个思路借鉴 vue-element-admin 项目。

### 平台管理
> rbac功能，这个功能的数据库是用的 django 自建的关系表，会不满足 dba 的要求，这个看看要不要自己手动改 \
> 权限控制，之前的版本是写在代码里，这次想写入数据库，考虑要不要用缓存，每次请求都会查库，但这个不清楚会不会有压力 \
> 审计，最早做过一版是手动写，这个太容易放弃了，需要中间接来做最合适 \
> 前后端菜单页面控制功能，这个要考虑下兜底问题，会导致页面配置异常，加载菜单报错。
- 用户管理: 提供用户的相关配置及用户筛选，新增用户后，默认密码为123456
- 角色管理: 对权限进行分配，可依据实际需要设置角色
- 权限管理: 权限自由控制，增删改查等
- 部门管理: 可配置系统组织架构，树形表格展示
- 任务调度: Cron任务管理

### 平台监控
- 在线用户: 在线用户监控
- IP黑名单: 实现系统IP黑名单拉黑功能
- CRUD日志: 实现CRUD日志记录功能(打算去除)
- 错误日志: 显示后台未知错误及其详情信息
- 服务监控: 实时监控查看后台服务器性能

### 资产管理
- 服务器管理: 服务器增删改查
- 网络设备: 待实现
- 存储设备: 待实现
- 安全设备: 待实现

### 工作管理
- 我的空间: 待实现
- 需求管理: 待实现
- 用户反馈

### 系统工具
- 系统接口: 展示后台接口--Swagger

### 基础功能
- page分页
- response结构化
- jwt 永久token创建


### 高级功能
- 类似 jumpserver 的链接功能
- cmdb 的功能，至少有个多云资源管理查询页面

### celery-beat
- 异步任务
- 定时任务功能
- 管理界面，不能再用 admin 的那个页面了，太矬了


## 项目方案
- 后端python3.8, django4.2
- 后端借鉴 [drf_admin](https://github.com/TianPangJi/drf_admin)
- 前端 vue3, antd, ts(其实ts我不会，但上了vue3都是强推ts的，那就跟进下) [vue-vben-admin](https://github.com/vbenjs/vue-vben-admin)
- 前端 admin 的模板地址 [vben-admin-thin-next](https://github.com/vbenjs/vben-admin-thin-next)
- 前端开发文档 [vvbin doc](https://doc.vvbin.cn/guide/)


##### ts学习地址[TypeScript 入门教程](https://ts.xcatliu.com/basics/any.html)

pip3 freeze pip freeze > requirements.txt

目前只安装了
- Django==4.2
- djangorestframework==3.14.0

[djangorestframework doc](https://www.django-rest-framework.org/tutorial/quickstart/)


```
├── celery_task                # Celery异步任务
├── docs                       # 文档
├── opstools                  # 项目主文件
│   ├── apps                   # 项目app
│   ├── common                 # 公共接口
│   ├── media                  # 上传文件media
│   ├── settings               # 配置文件
│   ├── utils                  # 全局工具
│   │   ├── exceptions.py      # 异常捕获
│   │   ├── middleware.py      # 中间件
│   │   ├── models.py          # 基类models文件
│   │   ├── pagination.py      # 分页配置
│   │   ├── permissions.py     # RBAC权限控制
│   │   ├── routers.py         # 视图routers
│   │   ├── swagger_schema.py  # swagger
│   │   ├── views.py           # 基类视图
│   │   └── websocket.py       # WebSocket用户验证
│   ├── routing.py             # WebSocket路由
│   ├── urls.py                # 项目根路由
│   └── wsgi.py                # wsgi
├── .gitignore                 # .gitignore文件
├── init.json                  # 数据库基础数据文件
├── LICENSE                    # LICENSE
├── manage.py                  # 项目入口、启动文件
├── README.md                  # README
└── requirements.txt           # requirements文件
```

优化功能
django debug tool https://github.com/jazzband/django-debug-toolbar
https://pypi.org/project/django-sql-explorer/

coreapi 与 https://pypi.org/project/django-coreapi/ 对比优劣