from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from goods.models import Goods
from utils import constants
from utils.response import success
from .serializers import CartSerializer, CartGoodsSerializer


# Create your views here.


class CartViewSet(viewsets.GenericViewSet):
    """
        购物车管理
    """
    permission_classes = (IsAuthenticated,)

    # serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartSerializer
        else:  # GET
            return CartGoodsSerializer

    def create(self, request, *args, **kwargs):
        """
            加购

            请求参数示例：
            {
                "goods_id": 1,
                "count": 2,
                "unit_id": 1
            }
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success()

    def list(self, request, *args, **kwargs):
        """
            查询购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user

        redis_conn = get_redis_connection('cart')
        user_cart = redis_conn.hgetall('cart_%s' % user.id)

        goods_ids = map(lambda key: key.split(":")[0], user_cart.keys())

        goods_list = Goods.objects.filter(pk__in=goods_ids, is_delete=False, state=constants.GoodsState.ON_SALE.value)

        serializer = self.get_serializer(goods_list, many=True)
        records = serializer.data

        carts = dict()
        for key, value in user_cart.items():
            goods_id, unit_id = key.split(":")
            carts[goods_id] = {"checked_unit": unit_id, "count": value}

        for record in records:
            record.update(carts.get(record.id))

        return success(records)
