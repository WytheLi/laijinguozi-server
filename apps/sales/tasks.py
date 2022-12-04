import logging

import pytz
from datetime import datetime, timedelta

from celery import shared_task
from django.db import transaction
from django.utils.timezone import get_current_timezone

from sales.models import Orders, OrderDetails
from utils.constants import OrderState

logger = logging.getLogger('django')  # 获取日志器


@shared_task
def order_timeout_cancel():
    """
        订单超过30分钟未支付，自动取消。每分钟轮询该任务
    :return:
    """
    tz = get_current_timezone()
    all_unpaid_order = Orders.objects.filter(state=OrderState.UNPAID.value).all()
    for order in all_unpaid_order:
        try:
            with transaction.atomic():
                if order.create_time + timedelta(minutes=30) < datetime.now():
                    order.state = OrderState.CANCELED.value
                    order.save()

                    OrderDetails.objects.filter(order=order).select_for_update().update(state=OrderState.CANCELED.value)
        except Exception as e:
            logger.error('order_timeout_cancel error: %s' % e)
            transaction.rollback()
            continue
        else:
            transaction.commit()
