from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from utils.response import success
from .models import Areas
from .serializers import AreasSerializer
# Create your views here.


class AreasView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    pagination_class = None     # 以防配置了全局分页，这里禁用分页

    serializer_class = AreasSerializer

    def get_object(self):
        return Areas.objects.filter(parent=self.request.query_params.get('parent')).all()

    def get(self, request, *args, **kwargs):
        serializer_write = self.get_serializer(data=request.query_params)
        serializer_write.is_valid(raise_exception=True)

        areas = self.get_object()
        serializer = self.get_serializer(areas, many=True)

        return success(serializer.data)
