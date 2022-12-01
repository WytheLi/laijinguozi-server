from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from utils.constants import GoodsState
from .models import Material, Goods, Stock


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
        retail_unit = validated_data.get('retail_unit')
        mini_unit = validated_data.get('mini_unit')
        retail_unit_weight = validated_data.get('retail_unit_weight')
        mini_unit_weight = validated_data.get('mini_unit_weight')
        if any([purchase_unit, retail_unit, mini_unit, retail_unit_weight, mini_unit_weight]):
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
            'retail_unit': {'write_only': True},
            'mini_unit': {'write_only': True},
            'retail_unit_weight': {'write_only': True},
            'mini_unit_weight': {'write_only': True}
        }


class GoodsSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()
    sales_volume = serializers.SerializerMethodField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    state = serializers.IntegerField(read_only=True)
    has_stock = serializers.BooleanField(read_only=True)
    has_stock_retail = serializers.BooleanField(read_only=True)
    latest_shelf_time = serializers.BooleanField(read_only=True)

    class Meta:
        model = Goods
        fields = ('material', 'whole_piece_price', 'retail_price', 'whole_piece_discount_price', 'retail_discount_price',
                  'enable_whole_piece', 'enable_retail', 'whole_piece_launched_num', 'retail_launched_num', 'k', 'store',
                  'sales_volume', 'comments', 'state', 'has_stock', 'has_stock_retail', 'latest_shelf_time')

    def get_sales_volume(self, instance):
        if instance.sales_volume is not None and int(instance.sales_volume) == instance.sales_volume:
            return int(instance.sales_volume)
        else:
            return instance.sales_volume

    def create(self, validated_data):
        try:
            # 开启一个事务
            with transaction.atomic():
                # django.db.transaction.TransactionManagementError: An error occurred in the current transaction.
                # You can't execute queries until the end of the 'atomic' block.
                # 在事务中，不能执行查询语句
                save_id = transaction.savepoint()

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
        fields = ('material', 'whole_piece_price', 'retail_price', 'whole_piece_discount_price', 'retail_discount_price',
                  'enable_whole_piece', 'enable_retail', 'whole_piece_launched_num', 'retail_launched_num', 'k', 'store')


class GoodsStateChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ('state',)

    def update(self, instance, validated_data):
        """
            商品状态变更
            TODO 状态变更日志
        :param instance:
        :param validated_data:
        :return:
        """
        state = validated_data.get('state')
        if (state in GoodsState.CHECKED.value and instance.state == GoodsState.UN_CHECKED.value) or \
                (state == GoodsState.UN_SALE.value and instance.state == GoodsState.ON_SALE.value):
            instance.state = state
        elif (state == GoodsState.ON_SALE.value and instance.state in [GoodsState.APPROVE.value, GoodsState.UN_SALE.value]):
            if (instance.enable_whole_piece and instance.has_stock) or (instance.enable_retail and instance.has_stock_retail):
                instance.state = state  # 上架
                instance.latest_shelf_time = datetime.now()
            else:
                raise serializers.ValidationError('商品库存为0，不能上架!')
        else:
            raise serializers.ValidationError('状态修改失败！')
        instance.save()
        return instance


class AddStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('goods', 'stock')

    def update(self, instance, validated_data):
        goods = validated_data.get('goods')
        stock = validated_data.get('stock')
        origin_stock = instance.stock   # 修改前库存。ps:注意这是查询操作不能写在事务块内
        final_stock = origin_stock + stock  # 修改后库存
        try:
            with transaction.atomic():
                Stock.objects.filter(goods=goods, stock=origin_stock).select_for_update().update(stock=final_stock)

                instance.goods.has_stock_retail = True
                if instance.whole_piece_stock:
                    instance.goods.has_stock = True
                instance.goods.save()
        except Exception as e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
        return instance

    def create(self, validated_data):
        try:
            with transaction.atomic():
                stock = Stock.objects.select_for_update().create(**validated_data)

                stock.goods.has_stock_retail = True
                if stock.whole_piece_stock:
                    stock.goods.has_stock = True
                stock.goods.save()
        except Exception as e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
        return stock
