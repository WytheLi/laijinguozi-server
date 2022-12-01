import os
import time
from decimal import Decimal

from django.db import models

from goods.models import Store, Goods, GoodsUnit
from users.models import Users, DeliveryAddress
from utils.models import BaseModel

# Create your models here.


class Orders(BaseModel):

    STATE_CHOICES = (
        (1, '已收货'),  # finish
        (2, '待支付'),
        (3, '已取消'),
        (4, '待配送')
    )

    DELIVER_TYPE_CHOICES = (
        (1, '送货上门'),
        (2, '自提'),
        (3, '快递')
    )

    # 暂时先接通微信，后续根据业务进行拓展
    PAY_TYPE_CHOICES = (
        (1, '微信'),
        (2, '支付宝')
    )

    parent_id = models.ForeignKey('self', models.PROTECT, verbose_name='关联父订单id')   # 如记录为父订单，值为0
    bill_number = models.CharField(max_length=24, unique=True, verbose_name='订单编号')
    user_id = models.ForeignKey(Users, models.SET_NULL, verbose_name='用户')
    username = models.CharField(max_length=32, verbose_name='用户名')
    store = models.ForeignKey(Store, models.SET_NULL, verbose_name='店铺')
    store_name = models.CharField(max_length=32, verbose_name='店铺名')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    pay_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='实际支付金额')
    deliver_type = models.SmallIntegerField(choices=DELIVER_TYPE_CHOICES, verbose_name='配送方式')
    freight = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='配送费')
    deliver_person = models.ForeignKey(Users, models.SET_NULL, related_name='deliver_orders', verbose_name='配送员')
    address = models.ForeignKey(DeliveryAddress, models.SET_NULL, verbose_name='收货地址')
    state = models.SmallIntegerField(choices=STATE_CHOICES, verbose_name='订单状态')
    pay_time = models.DecimalField(verbose_name='支付时间')
    pay_number = models.CharField(max_length=64, verbose_name='支付单号')
    pay_type = models.SmallIntegerField(choices=PAY_TYPE_CHOICES, default=1, verbose_name='支付方式')
    message = models.CharField(max_length=16, verbose_name='留言')    # 防止恶意备注，消耗小票，限制小一点
    is_delete = models.BooleanField(default=False, verbose_name='删除')
    pickup_code = models.CharField(max_length=4, verbose_name='自提取货码')      # 自提单，店内需要签字
    is_first = models.BooleanField(default=False, verbose_name='首单')

    integral = models.IntegerField(default=0, verbose_name='使用积分')
    integral_deduct_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='积分抵扣金额')

    express_company = models.IntegerField(verbose_name='快递公司')
    express_company_name = models.CharField(verbose_name='快递公司名称')
    express_number = models.CharField(max_length=64, verbose_name='快递单号')

    def get_order_no(self):
        is_debug = os.getenv("DEBUG", None)
        tmp = str(time.time()).split('.')
        user_id = str(self.user_id)
        completion_digits = 24 - len(user_id)
        if is_debug is True:
            completion_digits = 23 - len(user_id)
        completion_user_id = user_id.zfill(completion_digits)
        tmp.insert(1, completion_user_id)
        if is_debug is True:
            tmp.insert(0, '0')
        order_no = ''.join(tmp)
        return order_no


class OrderDetails(BaseModel):
    order_id = models.ForeignKey(Orders, models.CASCADE, verbose_name='订单ID')
    goods_id = models.ForeignKey(Goods, models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价')
    num = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='数量')
    unit = models.ForeignKey(GoodsUnit, models.SET_NULL, verbose_name='单位')
    user_id = models.ForeignKey(Users, models.SET_NULL, verbose_name='用户')  # 冗余用户id,便于商品的销售统计

    integral = models.IntegerField(default=0, verbose_name='使用积分')
    integral_deduct_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='积分抵扣金额')


class ReturnOrders(BaseModel):
    pass


class ReturnOrderDetails(BaseModel):
    pass
