from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from utils.response import success
from .serializers import CreateOrderSerializer

# Create your views here.


class OrderViewSet(GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CreateOrderSerializer

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
                    "total_price": 54,
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
