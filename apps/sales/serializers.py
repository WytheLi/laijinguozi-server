from rest_framework import serializers

from sales.models import Orders, OrderDetails


class OnlyWriteOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        fields = ('goods', 'price', 'num', 'retail_num', 'unit')


class CreateOrderSerializer(serializers.ModelSerializer):
    order_details = OnlyWriteOrderDetailSerializer(many=True)
    # bill_number = serializers.CharField(read_only=True, label='订单号')
    # pay_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True, label='实际支付金额')
    # state = serializers.BooleanField(read_only=True, label='订单状态')
    # pay_time = serializers.DateTimeField(label='支付时间')
    # pay_number = serializers.CharField(read_only=True, label='支付单号')
    # pickup_code = serializers.CharField(read_only=True, label='自提取货码')
    # is_first = serializers.BooleanField(read_only=True, label='首单')

    class Meta:
        model = Orders
        fields = ('order_details', 'store', 'total_price', 'deliver_type', 'address', 'message', 'integral', 'integral_deduct_price')
                  # 'bill_number', 'pay_price', 'state', 'pay_time', 'pay_number', 'pickup_code', 'is_first')

    def validate(self, attrs):
        """
            1、配送方式不为自提时，收货地址必填。
            2、使用的积分不大于用户积分
        :param attrs:
        :return:
        """

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        order_details = validated_data.get('order_details')
