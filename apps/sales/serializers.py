from rest_framework import serializers
from django.db import transaction

from sales.models import Orders, OrderDetails
from users.models import DeliveryAddress
from utils.common import Apportion
from utils.constants import DeliverType


class OnlyWriteOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        fields = ('goods', 'price', 'num', 'unit')


class CreateOrderSerializer(serializers.ModelSerializer):
    order_details = OnlyWriteOrderDetailSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('order_details', 'store', 'deliver_type', 'address', 'message', 'integral')

    def validate(self, validated_data):
        """
            1、配送方式不为自提时，收货地址必填。
            2、使用的积分不大于用户积分
            3、下单数量不大于商品库存
        :param validated_data:
        :return:
        """
        user = self.context['request'].user

        if validated_data.get('deliver_type') != DeliverType.SELF_PICKUP.value and not validated_data.get('address'):
            raise serializers.ValidationError('配送方式不为自提时，收货地址必填！')
        if validated_data.get('integral') and validated_data.get('integral') > user.total_points:
            raise serializers.ValidationError('积分不足！')

        order_details = validated_data.get('order_details')

        # 转换成零售单位数量
        for record in order_details:
            goods_stock = record['goods'].stock_set.first().stock
            if record['unit'].id == record['goods'].material.retail_unit.id:
                if record['num'] > goods_stock:
                    raise serializers.ValidationError(f"{record['goods'].name}库存不足！")
            elif record['unit'].id == record['goods'].material.purchase_unit.id:
                if record['num'] * record['goods'].material.retail_unit_weight > goods_stock:
                    raise serializers.ValidationError(f"{record['goods'].name}库存不足！")
            else:
                raise serializers.ValidationError(f"{record['goods'].name}单位错误！")

        purchase_unit_map = {record['goods'].id: record['goods'].material.purchase_unit.id for record in order_details}
        retail_unit_map = {record['goods'].id: record['goods'].material.retail_unit.id for record in order_details}
        weight_map = {record['goods'].id: record['goods'].material.retail_unit_weight for record in order_details}

        validated_data.setdefault('purchase_unit_map', purchase_unit_map)
        validated_data.setdefault('retail_unit_map', retail_unit_map)
        validated_data.setdefault('weight_map', weight_map)
        return validated_data

    def create(self, validated_data):
        """
            创建订单
                1、创建订单
                2、创建订单明细。计算积分分摊、积分抵扣金额分摊
        :param validated_data:
        :return:
        """
        order_details = validated_data.pop('order_details')
        purchase_unit_map = validated_data.pop('purchase_unit_map')
        retail_unit_map = validated_data.pop('retail_unit_map')
        weight_map = validated_data.pop('weight_map')
        total_price = sum([record['price'] * record['num'] for record in order_details])
        integral = validated_data.get('integral')

        user = self.context['request'].user
        validated_data['user'] = user
        try:
            with transaction.atomic():
                order = Orders(**validated_data)
                order.bill_number = order.get_order_no()
                integral_deduct_price = order.calculate_integral_deduct_price()
                order.integral_deduct_price = integral_deduct_price
                order.total_price = total_price - integral_deduct_price
                order.save()

                integral_appo, integral_deduct_price_appo = (None, None)
                if integral:
                    integral_appo = Apportion(integral, total_price, len(order_details))
                    integral_deduct_price_appo = Apportion(integral_deduct_price, total_price, len(order_details))

                details = list()
                for record in order_details:
                    checked_unit = record.get('unit')
                    num = record.get('num')
                    goods = record.get('goods')
                    price = record.get('price')
                    purchase_unit_id = purchase_unit_map.get(goods.id)
                    retail_unit_id = retail_unit_map.get(goods.id)
                    retail_unit_weight = weight_map.get(goods.id)

                    order_detail = OrderDetails(**record)
                    order_detail.retail_num = num if checked_unit.id == retail_unit_id else num * retail_unit_weight
                    order_detail.user = user
                    order_detail.order = order
                    order_detail.integral = integral_appo.calc_should_divided(num * price) if integral_appo else 0
                    order_detail.integral_deduct_price = integral_deduct_price_appo.calc_should_divided(num * price) if integral_deduct_price_appo else 0
                    details.append(order_detail)
                OrderDetails.objects.bulk_create(details)

        except Exception as e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
        return order


class UserRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.username
        }


class DeliveryAddressRelatedField(serializers.RelatedField):

    def to_representation(self, delivery_address):
        data = {
            'province': delivery_address.province.name,
            'city': delivery_address.city.name,
            'district': delivery_address.district.name,
            'detailed_address': delivery_address.detailed_address,
            'longitude': delivery_address.longitude,
            'latitude': delivery_address.latitude,
            'mobile': delivery_address.mobile,
            'telephone': delivery_address.telephone
        }
        return data

    class Meta:
        model = DeliveryAddress
        fields = ('province', 'city', 'district', 'detailed_address', 'longitude', 'latitude', 'mobile', 'telephone')


class GoodsRelatedField(serializers.RelatedField):
    def to_representation(self, goods):
        data = {
            "id": goods.id,
            "brand_name": goods.material.brand.name,
            "name": goods.material.name,
            "code": goods.material.code,
            "images": goods.material.images
        }
        return data


class OrderDetailsSerializer(serializers.ModelSerializer):

    unit = serializers.CharField(read_only=True, source='unit.name')
    goods = GoodsRelatedField(read_only=True)

    class Meta:
        model = OrderDetails
        exclude = ('order', 'user', 'pay_time', 'state', 'is_delete')


class OrderDetailsRelatedField(serializers.RelatedField):
    def to_representation(self, order_detail):
        data = {
            "id": order_detail.goods.id,
            "images": order_detail.goods.material.images
        }
        return data


class OnlyReadOrderSerializer(serializers.ModelSerializer):
    """
        订单详情序列化器

        `RelatedField`和`ModelSerializer`都能处理嵌套的序列化，对于多层嵌套序列化`ModelSerializer`应该更为灵活一点。

            RelatedField必须重写`to_representation()方法。
            NotImplementedError: OrderDetailsRelatedFieldSerializer.to_representation() must be implemented for field.

        Django关联序列化，通过打印到控制台的SQL观察，全部为分步查询（否则是我的语法不当）。当多级关联时，容易有性能瓶颈。
    """
    user = UserRelatedField(read_only=True)
    store = serializers.CharField(read_only=True, source='store.name')
    deliver_person = serializers.CharField(read_only=True, source='deliver_person.name')
    address = DeliveryAddressRelatedField(read_only=True)
    order_details = OrderDetailsSerializer(read_only=True, many=True)   # OrderDetails中order外键需要添加related_name='order_details'，否则不生效。
    state = serializers.SerializerMethodField()
    deliver_type = serializers.SerializerMethodField()
    pay_type = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        exclude = ('is_delete',)

    def get_state(self, obj):
        return obj.state_text

    def get_deliver_type(self, obj):
        return obj.deliver_type_text

    def get_pay_type(self, obj):
        return obj.pay_type_text

    def get_count(self, obj):
        return obj.order_details.count()


class OnlyReadOrdersSerializer(serializers.ModelSerializer):
    """
        订单列表序列化器
    """
    order_details = OrderDetailsRelatedField(read_only=True, many=True)
    state = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('total_price', 'state', 'create_time', 'order_details', 'count')

    def get_state(self, obj):
        return obj.state_text

    def get_count(self, obj):
        return obj.order_details.count()
