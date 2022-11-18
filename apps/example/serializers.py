from rest_framework import serializers

from .models import Person, Group, PersonGroupRelation


class PersonGroupRelSerializers(serializers.ModelSerializer):

    class Meta:
        model = PersonGroupRelation
        fields = '__all__'


class PersonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class GroupSerializers(serializers.ModelSerializer):
    """
        所有组的所有用户数据
    """

    def to_representation(self, instance):
        """
            序列化添加额外字段，这里是多对多结构查询
        :param instance:
        :return:
        """
        representation = super(GroupSerializers, self).to_representation(instance)
        representation['members'] = []
        for i in PersonSerializers(instance.members, many=True).data:
            reason = PersonGroupRelSerializers(instance.persongrouprelation_set.get(group=instance.id, person=i['id'])).data['invite_reason']
            i['invite_reason'] = reason
            representation['members'].append(i)
        return representation

    class Meta:
        model = Group
        fields = '__all__'
