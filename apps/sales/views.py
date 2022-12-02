from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateOrderSerializer

# Create your views here.


class OrderViewSet(GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        """
            创建订单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
