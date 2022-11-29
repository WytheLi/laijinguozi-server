from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import OrderingFilter, SearchFilter

from utils.filter_backend import MaterialFilter
from utils.response import success
from .models import Material, Goods
from .serializers import MaterialSerializer, GoodsSerializer, CheckedMaterialCreateGoodsSerializer


# Create your views here.


class MaterialViewSet(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)

    serializer_class = MaterialSerializer

    queryset = Material.objects.filter(is_delete=False)

    # 排序、过滤
    filter_backends = [OrderingFilter, MaterialFilter]
    ordering_fields = ["id"]
    search_fields = ['name', 'code', 'brand__name']

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

        return success()

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
        return success()

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
        return success()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class GoodsViewSet(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)

    queryset = Goods.objects.filter(is_delete=False)

    # 排序，rest_framework.filters.OrderingFilter
    # 过滤（内置过滤类），rest_framework.filters.SearchFilter
    # 第三方过滤类，django_filters.rest_framework.DjangoFilterBackend
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    # 配置排序字段 /goods?ordering=-update_time
    ordering_fields = ['update_time', 'sales_volume', 'comments', 'material__name']
    # 配置过滤字段
    # 内置过滤，必须用search查询参数，支持模糊查询。/goods?search=猫山王
    search_fields = ['material__name', 'material__code', 'material__brand__name']

    # django_filters过滤。可以指定某个字段过滤，可以and多条件查询，但是不支持模糊查询。有点鸡肋，通常需要自定义重写。/goods?material__brand__name=猫山王&state=1
    # ps：旧版本为filter_fields字段，新版改为filterset_fields
    filterset_fields = ['state']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success(data=serializer.data)

    def get_serializer_class(self):
        material = self.request.data.get('material')
        if isinstance(material, int):
            return CheckedMaterialCreateGoodsSerializer
        else:
            return GoodsSerializer

    def create(self, request, *args, **kwargs):
        """
            创建商品
                {
                    "material": {
                        "code": "168172",
                        "name": "富士苹果",
                        "brand": 1,
                        "category": 1,
                        "origin": "中国山东",
                        "images": "http://123.com",
                        "description": "清甜爽口",
                        "purchase_unit": 2,
                        "sale_unit": 1,
                        "sale_unit_weight": 10
                    },
                    "original_price": 18,
                    "discount_price": 16,
                    "unit": 1,
                    "k": 3,
                    "store": 1
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
