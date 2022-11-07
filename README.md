### 环境
- python3.7
- django3.2

### 模块
```
cd apps
python ..\manage.py startapp users
```

### Sentry
定义： sentry是一个基于Django构建的现代化的实时事件日志监控、记录和聚合平台。错误追踪工具
- 部署服务：
> https://develop.sentry.dev/self-hosted/  
> https://github.com/getsentry/self-hosted/releases

- python客户端


### 项目配置文件的覆盖、读取
- 覆盖
- 读取
`django.conf.LazySettings`类懒加载，实现主要代码逻辑
```
mod = importlib.import_module('laijinguozi.settings')

for setting in dir(mod):
    if setting.isupper():
        setting_value = getattr(mod, setting)

        setattr(self, setting, setting_value)
```

### Django项目理解（想到一句写一句）
```
1、序列化器，不仅是序列化、反序列化的工具，同时隔离了view和model，所有的业务逻辑都应该在序列化器中实现。

```

### jwt token主动失效
1、token黑名单

使用黑名单缓存，在一定程度上破坏了JWT无状态的特性。但是实际上需要主动使JWT失效的占比很小，对存储、读写的开销很小。

2、给每个用户一一对应的secret_key，主动失效时修改用户的secret_key。

jwt验证特性就是不用在服务端存储token，极大的节省了存储读写的开销。为每个用户存储一个独立的secret_key，相较于存储token读写的频率降低，但是存储的开销还是较大。


### 参考文档
- Sentry的安装配置集成以及简单的使用
> https://www.jianshu.com/p/176ba74dcdc3

- Django3.2官方文档
> https://docs.djangoproject.com/zh-hans/3.2/

- django-environ官方文档
> https://django-environ.readthedocs.io/en/latest/quickstart.html

- 【Django】自定义认证后端ModelBackend，完成用户名、手机号、邮箱等多账号登录
> https://blog.csdn.net/qq_39147299/article/details/108544832

- Django 中celery定时任务的使用
> https://blog.csdn.net/qq_53582111/article/details/120207740

- Kuboard - Kubernetes 多集群管理界面
> https://kuboard.cn/

- django中request.user的由来
> https://zhuanlan.zhihu.com/p/415424659  
> [python懒加载的实现](https://blog.csdn.net/willluckysmile/article/details/111386643)

- JWT 的 Token 过期时间为什么没有生效
> https://blog.csdn.net/somenzz/article/details/120540453
