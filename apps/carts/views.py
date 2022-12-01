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

    def get_object(self):
        return Goods.objects.filter(pk__in=self.goods_ids, is_delete=False, state=constants.GoodsState.ON_SALE.value)

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
        user_cart = redis_conn.hgetall('cart_user:%s' % user.id)

        goods_ids = map(lambda key: key.decode().split(":")[0], user_cart.keys())
        self.goods_ids = goods_ids

        queryset = self.get_object()
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(queryset, many=True)

            records = self.construct_data(serializer.data, user_cart)
            return self.get_paginated_response(records)
        else:
            serializer = self.get_serializer(queryset, many=True)
            records = self.construct_data(serializer.data, user_cart)

        return success(records)

    def construct_data(self, records, user_cart):
        """
            构造购物车列表数据
        :param records:
        :param user_cart:
        :return:
        """
        carts = dict()
        for key, value in user_cart.items():
            goods_id, unit_id = key.decode().split(":")
            carts[goods_id] = {"checked_unit": unit_id, "count": value}

        for record in records:
            record.update(carts.get(str(record['id'])))
        return records
