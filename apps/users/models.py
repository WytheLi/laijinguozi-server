from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import BaseModel
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
    avatar = models.CharField(max_length=128, null=True, blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=7, null=True, blank=True, verbose_name='昵称')

    class Meta:
        db_table = 'fire_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_username(self):
        """
            默认用户名：fire_<uuid>
        """
        pass


class WechatUser(BaseModel):
    """
        微信用户
    """
    user = models.ForeignKey(Users, models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=128, unique=True, verbose_name='open_id')
    session_key = models.CharField(max_length=128, verbose_name='对用户数据进行 加密签名 的密钥')     # 项目统一用的 secret_key

    class Meta:
        db_table = 'fire_wechat_user'
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name
