"""
Django settings for laijinguozi project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-_ht@vhiv!6#%f-m@75@y2fc(g#&i$kvs!#m5tp%-c9^f*2hvh8'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-_ht@vhiv!6#%f-m@75@y2fc(g#&i$kvs!#m5tp%-c9^f*2hvh8')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'django_celery_beat',

    'users.apps.UsersConfig',
    'home.apps.HomeConfig',
    'goods.apps.GoodsConfig',
    'example.apps.ExampleConfig',
    'upload_file.apps.UploadFileConfig',
    'carts.apps.CartsConfig',
    'sales.apps.SalesConfig',
    'areas.apps.AreasConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',      # 否则引发报错：`Forbidden (CSRF cookie not set.)`
    'utils.middlewares.JwtTokenBlackMiddleware',  # 主动失效的token拒绝访问
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middlewares.ExceptionMiddleware',
]

ROOT_URLCONF = 'laijinguozi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'laijinguozi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
# 修改TIME_ZONE = 'Asia/Shanghai'后，数据库存储的还是UTC时区的时间，接口返回前端时转换为本地时区。这里希望数据库存储的也是本地时间
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# 静态文件存放目录
STATIC_ROOT = './static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-rest-framework
REST_FRAMEWORK = {
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    # 限流
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    #     'utils.throttle.SmsRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '20/min',    # 匿名用户，每分钟请求超过20次会限流
    #     'user': '60/min',    # 认证用户，每分钟请求超过60次会限流
    #     'sms_code': '1/m',  # 短信验证码，每分钟请求超过1次会限流
    # },
    # 自定义分页器
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.PagePagination',
}

# JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 有效期
    'JWT_AUTH_HEADER_PREFIX': 'JWT-TOKEN',  # jwt前缀，默认为JWT
}

# SENTRY
SENTRY_DSN = os.getenv('SENTRY_DSN')

# 自定义用户类
AUTH_USER_MODEL = 'users.Users'

# 自定义登陆校验类
AUTHENTICATION_BACKENDS = ['utils.authenticated.AuthenticatedBackend']

# redis cache
redis_hostname = os.getenv('REDIS_HOSTNAME', '127.0.0.1')
redis_port = os.getenv('REDIS_PORT', 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_hostname}:{redis_port}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # token黑名单
    "token_blacklist": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_hostname}:{redis_port}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 有效的文件上传凭证
    "valid_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_hostname}:{redis_port}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 购物车
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_hostname}:{redis_port}/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的logger实例，默认True，禁用
    'formatters': {
        # 日志格式
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.getenv('LOG_PATH', os.path.join(BASE_DIR, 'logs')), '{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True  # 日志是否向上级传递。True 向上级传，False 不向上级传。默认为True。
        },
    }
}

# 设置django shell环境（默认为python shell），这里设置为ipython，支持自动补全、自动缩进等
# pip install ipython -i https://pypi.douban.com/simple
SHELL_PLUS = 'ipython'

# Celery
# Broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/15'
# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/15'
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 时区配置
CELERY_TIMEZONE = TIME_ZONE
# Celery日志。uwsgi启动celery该配置不生效
CELERY_CELERYD_LOG_FILE = os.path.join(os.getenv('LOG_PATH', os.path.join(BASE_DIR, 'logs')), "celery_work.log")
CELERY_CELERYBEAT_LOG_FILE = os.path.join(os.getenv('LOG_PATH', os.path.join(BASE_DIR, 'logs')), "celery_beat.log")
# 定时任务、周期性任务
CELERY_BEAT_SCHEDULE = {
    # 'mul_every_10_seconds': {
    #     'task': 'example.tasks.mul',  # 任务路径
    #     'schedule': 10,     # 每10秒执行一次
    #     'args': (14, 5)
    # },
    'order_timeout_cancel_every_60_seconds': {
        'task': 'sales.tasks.order_timeout_cancel',
        'schedule': 60,
    },
}
