from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Users(AbstractUser):
    """
        用户：
            - 顾客
            - 内部员工
        ps: 通过权限判断是否能登录小程序、App、Web端
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    wx_open_id = models.CharField(max_length=128, verbose_name="微信openId")
    is_employee = models.BooleanField(default=False, verbose_name="是否为内部员工")

    class Meta:
        db_table = 'fire_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
