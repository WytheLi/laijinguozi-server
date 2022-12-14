from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from utils.constants import GoodsState
from .models import Material, Goods, Stock


class BrandRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "id": value.id,
            "name": value.name
        }
        return data


class GoodsCategoryRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "id": value.id,
            "name": value.name
        }
        return data


class GoodsUnitRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "id": value.id,
            "name": value.name
        }
        return data


class OnlyReadMaterialSerializer(serializers.ModelSerializer):
    brand = BrandRelatedField(read_only=True)
    category = GoodsCategoryRelatedField(read_only=True)
    purchase_unit = GoodsUnitRelatedField(read_only=True)
    retail_unit = GoodsUnitRelatedField(read_only=True)
    mini_unit = GoodsUnitRelatedField(read_only=True)

    class Meta:
        model = Material
        exclude = ('is_delete',)


class StockRelatedField(serializers.RelatedField):

    def to_representation(self, stock):
        return {
            "stock": stock.stock,
            "lock_stock": stock.lock_stock
        }


class OnlyReadGoodsSerializer(serializers.ModelSerializer):
    material = OnlyReadMaterialSerializer()
    stock = StockRelatedField(read_only=True, many=True)
    sales_volume = serializers.SerializerMethodField(read_only=True)

    def get_sales_volume(self, instance):
        if instance.sales_volume is not None and int(instance.sales_volume) == instance.sales_volume:
            return int(instance.sales_volume)
        else:
            return instance.sales_volume

    class Meta:
        model = Goods
        exclude = ('is_delete',)


class OnlyWriteMaterialSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        material = Material(**validated_data)
        material.spec = material.spec_text
        material.save()
        return material

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)

        # ???????????????????????????
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
        exclude = ('spec', 'is_delete')


class OnlyWriteGoodsSerializer(serializers.ModelSerializer):
    material = OnlyWriteMaterialSerializer()

    class Meta:
        model = Goods
        fields = ('material', 'whole_piece_price', 'retail_price', 'whole_piece_discount_price', 'retail_discount_price',
                  'enable_whole_piece', 'enable_retail', 'whole_piece_launched_num', 'retail_launched_num', 'k', 'store')

    def create(self, validated_data):
        try:
            # ??????????????????
            with transaction.atomic():
                # django.db.transaction.TransactionManagementError: An error occurred in the current transaction.
                # You can't execute queries until the end of the 'atomic' block.
                # ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????filter()???get()???
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


class GoodsStateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ('state',)

    def update(self, instance, validated_data):
        """
            ??????????????????
            TODO ??????????????????
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
                instance.state = state  # ??????
                instance.latest_shelf_time = datetime.now()
            else:
                raise serializers.ValidationError('???????????????0???????????????!')
        else:
            raise serializers.ValidationError('?????????????????????')
        instance.save()
        return instance


class GoodsStateBulkUpdateListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        if len(instance) != len(self.child.initial_data):
            raise serializers.ValidationError('?????????????????????')

        goods_map = {goods.id: goods for goods in instance}
        data_map = {item['id']: item for item in self.child.initial_data}

        ret = []
        for goods_id, data in data_map.items():
            goods = goods_map.get(goods_id, None)
            if goods:
                if not (goods.state == GoodsState.UN_CHECKED.value and data['state'] in GoodsState.CHECKED.value) \
                    or not (goods.state == GoodsState.ON_SALE.value and data['state'] == GoodsState.UN_SALE.value) \
                        or not (goods.state in [GoodsState.APPROVE.value, GoodsState.UN_SALE.value] and data['state'] == GoodsState.ON_SALE.value):
                    raise serializers.ValidationError(f'{goods.material.name}')
            ret.append(self.child.update(goods, data))
        return ret


class GoodsStateBulkUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = GoodsStateBulkUpdateListSerializer
        model = Goods
        fields = ('state',)


class AddStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('goods', 'stock')

    def update(self, instance, validated_data):
        goods = validated_data.get('goods')
        stock = validated_data.get('stock')
        origin_stock = instance.stock   # ??????????????????ps:????????????????????????????????????????????????
        final_stock = origin_stock + stock  # ???????????????
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
