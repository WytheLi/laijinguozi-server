from rest_framework import serializers

from .models import Material


class MaterialSerializers(serializers.ModelSerializer):

    brand_name = serializers.CharField(read_only=True, source='brand.name')
    category_name = serializers.CharField(read_only=True, source='category.name')
    unit_name = serializers.CharField(read_only=True, source='unit.name')

    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ('brand_name', 'category_name', 'unit_name')
        extra_kwargs = {
            'is_delete': {'write_only': True},
            'brand': {'write_only': True},
            'category': {'write_only': True},
            'unit': {'write_only': True}
        }
