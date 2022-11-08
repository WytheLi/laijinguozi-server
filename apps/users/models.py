from decimal import Decimal

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
    is_employee = models.BooleanField(default=False, verbose_name="是否为内部员工")
    avatar = models.CharField(max_length=128, null=True, blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=7, null=True, blank=True, verbose_name='昵称')
    total_points = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='总积分')

    class Meta:
        db_table = 'fruits_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_username(self):
        """
            默认用户名：fruits_<uuid>
        """
        pass


class WechatUser(BaseModel):
    """
        微信用户
    """
    user = models.ForeignKey(Users, models.PROTECT, null=True, blank=True,  verbose_name='用户')
    openid = models.CharField(max_length=128, unique=True, verbose_name='open_id')
    session_key = models.CharField(max_length=128, verbose_name='对用户数据进行 加密签名 的密钥')     # 项目统一用的 secret_key

    class Meta:
        db_table = 'fruits_wechat_user'
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name


class DeliveryAddress(BaseModel):
    """
        用户的收货地址
    """
    user = models.ForeignKey(Users, models.CASCADE, related_name='address', verbose_name='用户')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district', verbose_name='区')
    detailed_address = models.CharField(max_length=256, verbose_name='详细地址')
    longitude = models.CharField(max_length=32, null=True, blank=True, verbose_name='经度')
    latitude = models.CharField(max_length=32, null=True, blank=True, verbose_name='纬度')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    telephone = models.CharField(max_length=10, null=True, blank=True, verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    is_default = models.BooleanField(default=False, verbose_name='默认地址')

    class Meta:
        db_table = 'fruits_delivery_address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name


class Logs(BaseModel):

    action_map = {
        'pay_points': 1,
        'comment_points': 2,
        'points_deduction': 3,
        'on_sale': 4,
        'off_sale': 5
    }

    ACTION_ENUM = (
        (1, '下单获取积分'),
        (2, '评论获取积分'),
        (3, '积分抵扣'),
        (4, '商品上架'),
        (5, '商品下架'),
    )

    handler = models.ForeignKey(Users, models.CASCADE, related_name='manipulator', verbose_name='处理人')
    handler_name = models.CharField(max_length=32, verbose_name='处理人名称')
    affected_id = models.IntegerField(verbose_name='受影响对象id')
    type = models.SmallIntegerField(choices=((1, '用户积分日志'), (2, '商品上下架日志'), (3, '商品价格修改日志'), (4, '储值卡消费日志')), verbose_name='类型')
    action = models.IntegerField(choices=ACTION_ENUM, verbose_name='action')
    do = models.CharField(max_length=16, verbose_name='做了啥')
    before = models.CharField(max_length=16, verbose_name='单据完成之前')
    after = models.CharField(max_length=17, verbose_name='单据完成之后')

    class Meta:
        db_table = 'fruits_logs'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
