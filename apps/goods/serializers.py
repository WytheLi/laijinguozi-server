from rest_framework import serializers

from .models import Material


class MaterialSerializers(serializers.ModelSerializer):

    brand_name = serializers.CharField(read_only=True, source='brand.name')
    category_name = serializers.CharField(read_only=True, source='category.name')

    def create(self, validated_data):
        instance = Material(**validated_data)
        instance.spec = self.get_spec(instance)
        instance.save()
        return instance

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
            instance.spec = self.get_spec(instance)

        instance.save()
        return instance

    def get_spec(self, instance):
        return f'1{instance.purchase_unit.name}' \
               f'*{instance.sale_unit_weight}{instance.sale_unit.name}' \
               f'*{instance.mini_unit_weight}{instance.mini_unit.name}' \
                if instance.mini_unit_weight else f'1{instance.purchase_unit.name}*{instance.sale_unit_weight}{instance.sale_unit.name}'

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
