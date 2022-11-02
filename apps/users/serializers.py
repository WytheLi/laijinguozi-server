from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext as _

from users.models import Users

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'username', 'mobile', 'email', 'avatar', 'nickname', 'is_employee')


class JwtTokenSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        wx_open_id = attrs.get('wx_open_id')

        if wx_open_id:
            # TODO 微信登录
            if lambda x: True:
                user = Users.objects.get(wx_open_id=wx_open_id)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),   # 生成jwt token
                    'user': user
                }

            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{wx_open_id}" and "password".')
            msg = msg.format(wx_open_id=attrs.get('wx_open_id'))
            raise serializers.ValidationError(msg)

    class Meta:
        model = Users
        fields = ('wx_open_id',)
