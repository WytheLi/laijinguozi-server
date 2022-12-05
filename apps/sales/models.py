import os
import time
from decimal import Decimal

from django.db import models

from goods.models import Store, Goods, GoodsUnit
from users.models import Users, DeliveryAddress
from utils.constants import OrderState
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

    bill_number = models.CharField(max_length=24, unique=True, verbose_name='订单编号')
    user = models.ForeignKey(Users, models.CASCADE, verbose_name='用户')
    store = models.ForeignKey(Store, models.CASCADE, verbose_name='店铺')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='合计')    # 减去优惠后的金额
    pay_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='实际支付金额')
    deliver_type = models.SmallIntegerField(choices=DELIVER_TYPE_CHOICES, verbose_name='配送方式')
    freight = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='配送费')
    deliver_person = models.ForeignKey(Users, models.CASCADE, related_name='deliver_orders', default=1, verbose_name='配送员')
    # deliver_time_interval = models.ForeignKey(DeliverTimeInterval, models.CASCADE, verbose_name='配送上门的时间段')
    address = models.ForeignKey(DeliveryAddress, models.CASCADE, null=True, blank=True, verbose_name='收货地址')
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=OrderState.UNPAID.value, verbose_name='订单状态')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    pay_number = models.CharField(max_length=64, null=True, blank=True, verbose_name='支付单号')
    pay_type = models.SmallIntegerField(choices=PAY_TYPE_CHOICES, default=1, verbose_name='支付方式')
    message = models.CharField(max_length=16, null=True, blank=True, verbose_name='留言')    # 防止恶意备注，消耗小票，限制小一点
    is_delete = models.BooleanField(default=False, verbose_name='删除')
    pickup_code = models.CharField(max_length=4, null=True, blank=True, verbose_name='自提取货码')      # 自提单，店内需要签字
    is_first = models.BooleanField(default=False, verbose_name='首单')

    integral = models.IntegerField(default=0, verbose_name='使用积分')
    integral_deduct_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='积分抵扣金额')

    # express_company = models.IntegerField(verbose_name='快递公司')
    # express_company_name = models.CharField(max_length=8, null=True, blank=True, verbose_name='快递公司名称')
    # express_number = models.CharField(max_length=64, null=True, blank=True, verbose_name='快递单号')

    class Meta:
        db_table = 'fruits_orders'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def get_order_no(self):
        """
            生成24位订单号
        :return:
        """
        is_debug = os.getenv("DEBUG", None)
        tmp = str(time.time()).split('.')
        user_id = str(self.user_id)
        completion_digits = 8 - len(user_id)
        if is_debug == 'True':
            completion_digits = 7 - len(user_id)
        completion_user_id = user_id.zfill(completion_digits)
        tmp.insert(1, completion_user_id)
        if is_debug == 'True':
            tmp.insert(0, '0')
        order_no = ''.join(tmp)
        return order_no

    def calculate_integral_deduct_price(self):
        """
            计算积分抵扣金额，100积分抵扣1元
        :return:
        """
        return self.integral / Decimal('100.00') if self.integral else 0

    @property
    def state_text(self):
        state_map = {key: val for key, val in self.STATE_CHOICES}
        return state_map.get(self.state)

    @property
    def deliver_type_text(self):
        deliver_type_map = {key: val for key, val in self.DELIVER_TYPE_CHOICES}
        return deliver_type_map.get(self.deliver_type)

    @property
    def pay_type_text(self):
        pay_type_map = {key: val for key, val in self.PAY_TYPE_CHOICES}
        return pay_type_map.get(self.pay_type)


class OrderDetails(BaseModel):

    STATE_CHOICES = (
        (1, '已收货'),  # finish
        (2, '待支付'),
        (3, '已取消'),
        (4, '待配送')
    )

    order = models.ForeignKey(Orders, models.CASCADE, related_name='order_details', verbose_name='订单ID')
    goods = models.ForeignKey(Goods, models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价')
    num = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='数量')
    retail_num = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='零售单位数量')
    unit = models.ForeignKey(GoodsUnit, models.CASCADE, verbose_name='单位')
    # 冗余用户id、支付日期、状态等字段，方便商品的销售统计v2.0
    user = models.ForeignKey(Users, models.CASCADE, verbose_name='用户')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    state = models.SmallIntegerField(default=OrderState.UNPAID.value, verbose_name='订单状态')
    is_delete = models.BooleanField(default=False, verbose_name='删除')

    # 部分退款时，退积分、退钱。
    integral = models.IntegerField(default=0, verbose_name='使用积分')
    integral_deduct_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='积分抵扣金额')

    class Meta:
        db_table = 'fruits_order_details'
        verbose_name = '订单明细'
        verbose_name_plural = verbose_name

    @property
    def state_text(self):
        state_map = {key: val for key, val in self.STATE_CHOICES}
        return state_map.get(self.state)


class ReturnOrders(BaseModel):
    pass


class ReturnOrderDetails(BaseModel):
    pass
