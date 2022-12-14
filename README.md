### 环境
- python3.6.13
- django3.2

### 版本迭代
#### v1.0
1. 完成商品模块，商品的增、删、改、查。
2. 完成商品状态的修改，审核、上下架
3. 完成文件上传服务，管理商品图片、用户头像、活动轮播图等资源的存储
4. 完成购物车加购，勾选购物车商品计算积分抵扣优惠
5. 完成库存补货，库存流水记录
6. 完成订单下单、微信支付、退款（整单退款、部分退款视情况而定）
7. 完成库存小于日均销量的20%短信提示补货
8. 完成操作日志，价格修改日志、商品上下架日志、用户积分日志。

### Dockerfile部署django和celery服务
> https://cloud.tencent.com/developer/article/1926787

### 清除所有项目目录/migrations/下除`__init__.py`文件之外的py文件
```
find . -path "*migrations*" -name "*.py" -not -path "*__init__*" -exec rm {} \;
```

### Git空文件夹管理
Git默认不支持空文件的管理，如果想在Git仓库中提交空文件夹，常用做法是在空文件下新建一个`.gitkeep`文件

(1).查找当前目录下所有的空文件夹
`find . -type -d -empty`
(2).查找当前目录下所有的空文件夹并新建一个.gitkeep空文件
`find . -type -d -empty -exec touch {}/.gitkeep \;`


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


### jwt token主动失效
1、token黑名单

使用黑名单缓存，在一定程度上破坏了JWT无状态的特性。但是实际上需要主动使JWT失效的占比很小，对存储、读写的开销很小。

2、给每个用户一一对应的secret_key，主动失效时修改用户的secret_key。

jwt验证特性就是不用在服务端存储token，极大的节省了存储读写的开销。为每个用户存储一个独立的secret_key，相较于存储token读写的频率降低，但是存储的开销还是较大。


### postman tests
```
console.log('tests running...');
var jsonData = JSON.parse(responseBody);
// console.log(pm.response);
if (pm.response.code == 200 || pm.response.code == 201) {
    pm.environment.set("token", 'JWT-TOKEN ' + jsonData.data.token);
}
```

### django orm VS SQLAlchemy
1、实际的项目中Django和SQLAlchemy结合使用，Django用于所有常规的CRUD操作，而SQLAlchemy用于更复杂的查询，“业务规则”和限制条件较多的查询，如各类报表等只读查询。


### 文件服务
使用`go-fastdfs`和`go-fastdfs-web`镜像
- 部署go-fastdfs
```
docker pull sjqzhang/go-fastdfs

docker run -d --name go-fastdfs -v /opt/go-fastdfs:/data -p 8085:8080 -e GO_FASTDFS_DIR=/data sjqzhang/go-fastdfs
1.运行后查看本地映射中文件夹是否出现conf data files 等文件夹
2.修改白名单，修改本地映射中文件夹conf/cfg.json 文件内容中的"admin_ips"字段 所有人可访问修改为“0.0.0.0”

docker restart fastdfs
测试是否正常：访问 http://本地ip:8080
```

- 部署go-fastdfs-web
```
docker pull perfree/fastdfsweb

docker run --name go-fastdfs-web -d -p 8086:8088 perfree/fastdfsweb
测试是否正常访问 http://本地ip:8088 

配置go-fastdfs-web
集群名称：随意填写
组：对应本地映射中文件夹conf/cfg.json 文件内容中的group
服务地址：http://本地ip:8080
访问地址：http://本地ip:8080
用户名密码邮箱。自己填写创建
```
> https://sjqzhang.github.io/go-fastdfs/install.html#docker


### 全国省市县行政区划SQL代码文件参考
> https://shopmini.oss-accelerate.aliyuncs.com/city.sql

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

Celery执行异步和周期性任务
> https://zhuanlan.zhihu.com/p/369639432

```
 Django==3.2
 celery==5.0.5
 redis==3.5.3
 
 # 可选，windows下运行celery 4以后版本，还需额外安装eventlet库
 eventlet 
 # 推荐安装, 需要设置定时或周期任务时安装，推荐安装
 django-celery-beat==2.2.0
 # 视情况需要，需要存储任务结果时安装，视情况需要
 django-celery-results==2.0.1
 # 视情况需要，需要监控celery运行任务状态时安装
 flower==0.9.7
```
启动Celery
```
 # Linux下测试，启动Celery
 celery -A laijinguozi worker -l info
 # Windows下测试，启动Celery
 celery -A laijinguozi worker -l info -P eventlet
 # 如果Windows下Celery不工作，输入如下命令
 celery -A laijinguozi worker -l info --pool=solo
```
> Error: Invalid value for '-A' / '--app':
> https://github.com/celery/celery/issues/6363

'--pool' 默认是prefork(并发)，选择solo之后，发送的任务不会被并发执行(串行)，在worker执行任务过程中，再次发送给worker的任务会排队，执行完一个再执行另一个

Celery5.0启动失败，降低版本至Celery4.4.0
> https://www.celerycn.io/fu-lu/django

启动任务调度器beat
```
celery -A laijinguozi beat -l info
```
> celery  root 用户无法启动。如果想强行启动，不用修改代码。直接：`export C_FORCE_ROOT="true"`

celery中task和share_task的区别
task：装饰函数，将函数当成celery的任务函数
share_task：
1. 装饰函数，将函数当成celery的任务函数，
2. 不依赖某个celery对象，而是加载到内存之后自动添加到celery对象中
3. 与多个celery对象进行关联


- Kuboard - Kubernetes 多集群管理界面
> https://kuboard.cn/

- django中request.user的由来
> https://zhuanlan.zhihu.com/p/415424659  
> [python懒加载的实现](https://blog.csdn.net/willluckysmile/article/details/111386643)

- JWT 的 Token 过期时间为什么没有生效
> https://blog.csdn.net/somenzz/article/details/120540453

- Django ORM Cookbook中文版
> https://django-orm-cookbook-zh-cn.readthedocs.io/zh_CN/latest/index.html


- EverSQL查询优化器
> https://www.eversql.com/

- 轻量级消息队列Django-Q
> [轻量级消息队列Django-Q初体验](https://www.django.cn/article/show-35.html)
> [Django Q官方文档](https://django-q.readthedocs.io/en/latest/index.html)



### 项目报错及对应的解决方案
创建订单时报错：外键约束失败
```
django.db.utils.IntegrityError: FOREIGN KEY constraint failed.
```
