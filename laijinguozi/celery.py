import os

from celery import Celery
# ImportError: cannot import name 'Celery' from 'celery'
# 解决方案：https://github.com/celery/celery/issues/7783
# 由于python版本缘故，python 3.7中importlib-metadata==5.0.0版本，降为4.12.0
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laijinguozi.settings')

celery_app = Celery('celeryApp')
# 允许你在Django配置文件中对Celery进行配置
# namespace='CELERY'，所有Celery配置项必须以CELERY_开头，防止冲突
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# 自动从settings的配置INSTALLED_APPS中的应用目录下加载tasks.py
celery_app.autodiscover_tasks()
celery_app.conf.update(
    accept_content=['json', 'pickle']
)
