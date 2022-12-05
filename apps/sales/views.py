from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from utils.constants import RequestType
from utils.response import success
from .models import Orders
from .serializers import CreateOrderSerializer, OnlyReadOrderSerializer, OnlyReadOrdersSerializer


# Create your views here.


class OrderViewSet(GenericViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = Orders.objects.filter(is_delete=False)

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['create_time']
    filterset_fields = ['state']

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.method == RequestType.GET.value:
            if self.kwargs.get('pk'):
                # 订单详情
                return OnlyReadOrderSerializer
            # 订单列表
            return OnlyReadOrdersSerializer
        else:
            return CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        """
            创建订单
                {
                    "order_details": [{
                        "goods": 1,
                        "price": 18,
                        "num": 3,
                        "unit": 1
                    }],
                    "store": 1,
                    "deliver_type": 2,
                    "message": "水果要新鲜，否则差评！",
                    "integral": 168
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
            UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'sales.models.Orders'> QuerySet.
            未排序的查询集，分页可能会产生不一致的结果。
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success(serializer.data)

    def get(self, request, *args, **kwargs):

        order = self.get_object()
        serializer = self.get_serializer(order)

        return success(serializer.data)


class OrderPaymentView(APIView):

    def post(self, request, *args, **kwargs):
        """
            订单支付
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def get(self, request, *args, **kwargs):
        """
            订单支付回调
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass
