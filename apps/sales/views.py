from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateOrderSerializer

# Create your views here.


class OrderViewSet(GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        pass
