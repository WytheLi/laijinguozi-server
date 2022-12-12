from decimal import Decimal

from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import Goods, Material, GoodsUnit


class CartSerializer(serializers.Serializer):
    goods_id = serializers.IntegerField(min_value=1, write_only=True)
    count = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True, label="加购数量")
    unit_id = serializers.IntegerField(min_value=1, write_only=True, label="勾选单位")

    def validate_count(self, count):
        if count <= 0:
            raise serializers.ValidationError('加购不能小于0！')
        return count

    def validate(self, attrs):
        try:
            goods = Goods.objects.get(pk=attrs['goods_id'])
            # goods = Goods.objects.prefetch_related('stock_set').get(pk=attrs['goods_id'])
        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在!')

        stock_obj = goods.stock.first()
        if not stock_obj or attrs['count'] > stock_obj.stock:
            raise serializers.ValidationError('商品库存不够！')
        return attrs

    def create(self, validated_data):
        goods_id = validated_data['goods_id']
        count = validated_data['count']
        unit_id = validated_data['unit_id']

        user = self.context['view'].request.user

        redis_conn = get_redis_connection('cart')
        # 购物车数据结构，cart_user<user_id> = {"goods_id:unit_id": count, }
        redis_conn.hincrbyfloat('cart_user:%s' % user.id, '%s:%s' % (goods_id, unit_id), float(count))
        return True


class CartGoodsMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('code', 'name', 'brand', 'purchase_unit', 'retail_unit', 'spec')


class CartGoodsSerializer(serializers.ModelSerializer):
    """
        购物车商品列表序列化器
    """
    material = CartGoodsMaterialSerializer()

    class Meta:
        model = Goods
        fields = ('material', 'whole_piece_price', 'retail_price', 'whole_piece_discount_price', 'retail_discount_price',
                  'enable_whole_piece', 'enable_retail', 'has_stock', 'has_stock_retail', 'id')


class CartCheckedListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        """
            计算最佳优惠
            1、统计总金额
            2、计算优惠
        :param attrs:
        :return:
        """
        total_price = 0
        for record in attrs:
            goods = record['goods']
            checked_unit = record['checked_unit']
            num = record['num']
            if goods.material.retail_unit == checked_unit:
                total_price += goods.retail_price * num
            elif goods.material.purchase_unit == checked_unit:
                total_price += goods.whole_piece_price * num
            else:
                raise serializers.ValidationError(f'{goods.material.name}单位错误！')

        # 用户积分最大抵扣
        user = self.context['request'].user
        integral_deduct_price = user.total_points / Decimal('100.00') if user.total_points else 0
        amount_after_discount = total_price - integral_deduct_price

        # 优惠后满68能下单
        has_place_order = True if amount_after_discount >= 68 else False

        data = {
            'total_price': total_price,
            'amount_after_discount': amount_after_discount,
            'has_place_order': has_place_order
        }
        return data


class CartCheckedSerializer(serializers.Serializer):

    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.filter(), write_only=True, required=True)
    checked_unit = serializers.PrimaryKeyRelatedField(queryset=GoodsUnit.objects.filter(), write_only=True, required=True)
    num = serializers.DecimalField(max_digits=8, decimal_places=2, write_only=True, required=True)

    class Meta:
        list_serializer_class = CartCheckedListSerializer
        fields = ('goods', 'checked_unit')
