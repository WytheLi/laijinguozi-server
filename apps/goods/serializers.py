from django.db import transaction
from rest_framework import serializers

from .models import Material, Goods


class MaterialSerializer(serializers.ModelSerializer):

    brand_name = serializers.CharField(read_only=True, source='brand.name')
    category_name = serializers.CharField(read_only=True, source='category.name')

    def create(self, validated_data):
        material = Material(**validated_data)
        material.spec = material.spec_text
        material.save()
        return material

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)

        # 规格改变，更新规格
        purchase_unit = validated_data.get('purchase_unit')
        sale_unit = validated_data.get('sale_unit')
        mini_unit = validated_data.get('mini_unit')
        sale_unit_weight = validated_data.get('sale_unit_weight')
        mini_unit_weight = validated_data.get('mini_unit_weight')
        if any([purchase_unit, sale_unit, mini_unit, sale_unit_weight, mini_unit_weight]):
            instance.spec = instance.spec_text

        instance.save()
        return instance

    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ('brand_name', 'category_name', 'spec')
        extra_kwargs = {
            'is_delete': {'write_only': True},
            'brand': {'write_only': True},
            'category': {'write_only': True},
            'purchase_unit': {'write_only': True},
            'sale_unit': {'write_only': True},
            'mini_unit': {'write_only': True},
            'sale_unit_weight': {'write_only': True},
            'mini_unit_weight': {'write_only': True}
        }


class GoodsSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()
    sales_volume = serializers.SerializerMethodField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    state = serializers.BooleanField(read_only=True)

    class Meta:
        model = Goods
        fields = ('material', 'original_price', 'discount_price', 'unit', 'k',
                  'maximum_purchase', 'minimum_purchase', 'store',
                  'sales_volume', 'comments', 'state')

    def get_sales_volume(self, instance):
        if instance.sales_volume is not None and int(instance.sales_volume) == instance.sales_volume:
            return int(instance.sales_volume)
        else:
            return instance.sales_volume

    def create(self, validated_data):
        # 开启一个事务
        with transaction.atomic():
            # django.db.transaction.TransactionManagementError: An error occurred in the current transaction.
            # You can't execute queries until the end of the 'atomic' block.
            # 在事务中，不能执行查询语句
            save_id = transaction.savepoint()
            try:
                material = Material(**validated_data['material'])
                material.spec = material.spec_text
                material.save()

                validated_data['material'] = material
                goods = Goods.objects.create(**validated_data)
            except serializers.ValidationError as e:
                raise e
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                raise e
            else:
                transaction.savepoint_commit(save_id)
        return goods


class CheckedMaterialCreateGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ('material', 'original_price', 'discount_price', 'unit', 'k',
                  'maximum_purchase', 'minimum_purchase', 'store')
