from rest_framework import serializers

from areas.models import Areas


class AreasSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(write_only=True, required=True, allow_null=False)

    class Meta:
        model = Areas
        fields = ('id', 'name', 'parent')
        read_only_fields = ('id', 'name')
