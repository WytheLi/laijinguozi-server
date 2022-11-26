from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from utils.response import success
from .models import Material
from .serializers import MaterialSerializers

# Create your views here.


class MaterialViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = MaterialSerializers

    queryset = Material.objects.filter(is_delete=False)

    def partial_update(self, request, *args, **kwargs):
        """
            修改物料
                rest_framework.mixins.UpdateModelMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        # partial=True: 序列化器不会对请求数据中缺少的字段进行字段验证检查,部分修改; partial=False: 全量修改
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return success(serializer.data)

    def create(self, request, *args, **kwargs):
        """
            新建物料
                rest_framework.mixins.CreateModelMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
            物料详情
                rest_framework.mixins.RetrieveModelMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success(serializer.data)

    def list(self, request, *args, **kwargs):
        """
            物料列表
                rest_framework.mixins.ListModelMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success(data=serializer.data)

    def destory(self, request, *args, **kwargs):
        """
            删除物料
                rest_framework.mixins.DestroyModelMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return success({})

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
