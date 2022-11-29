from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import Goods


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

        stock_obj = goods.stock_set.first()
        if not stock_obj or attrs['count'] > stock_obj.stock:
            raise serializers.ValidationError('商品库存不够！')
        return attrs

    def create(self, validated_data):
        goods_id = validated_data['goods_id']
        count = validated_data['count']
        unit_id = validated_data['unit_id']

        user = self.context['view'].request.user

        redis_conn = get_redis_connection('cart')
        # 购物车数据结构，cart_<user_id> = {"goods_id:unit_id": count, }
        redis_conn.hincrbyfloat('cart_%s' % user.id, '%s:%s' % (goods_id, unit_id), float(count))
        return True
