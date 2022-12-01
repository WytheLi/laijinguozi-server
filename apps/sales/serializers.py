from rest_framework import serializers

from sales.models import Orders, OrderDetails


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        fields = ('goods', 'price', 'num', 'retail_num', 'unit', 'user', 'integral', 'integral_deduct_price')


class CreateOrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('user', 'store', 'total_price', 'pay_price', 'deliver_type', 'address', 'pay_type', 'message',
                  'integral', 'integral_deduct_price')

    def create(self, validated_data):
        pass
