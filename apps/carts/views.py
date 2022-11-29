from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from utils.response import success
from .serializers import CartSerializer

# Create your views here.


class CartViewSet(viewsets.GenericViewSet):
    """
        购物车管理
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = CartSerializer

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

        Goods.objects.filter(pk__in=goods_ids)

        for key, value in user_cart.items():
            goods_id, unit_id = key.split(":")
            count = value





