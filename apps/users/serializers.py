from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import Users, WechatUser
from utils.wechat_sdk import wechat_login

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'username', 'mobile', 'email', 'avatar', 'nickname', 'is_employee')


class WechatLoginSerializer(serializers.Serializer):

    wx_code = serializers.CharField(write_only=True)
    mobile = serializers.CharField(max_length=11, write_only=True)

    def create(self, validated_data):
        wx_code = validated_data.pop('wx_code')
        mobile = validated_data.pop('mobile')

        session_key, openid = wechat_login.jscode2session(wx_code)

        wechat_user = WechatUser.objects.filter(openid=openid).select_related('user').first()
        if wechat_user:
            # 签发JWT token
            user = wechat_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.token = token
        else:
            user = Users.objects.get(mobile=mobile)

            WechatUser.objects.create(user=user, openid=openid, session_key=session_key)

            # 签发JWT token
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.token = token
        # 将token给到视图，用以响应给前端。
        # 因为context是实例化序列化器类的时候注入的。用来实现视图和序列化器之间的参数传递。
        # 这里validated_data只是一个形参，不能通过它去传递值，在validate(self, validated_data)可以是因为函数return了validated_data
        self.context['view'].user = user
        self.context['view'].token = token
        return user
