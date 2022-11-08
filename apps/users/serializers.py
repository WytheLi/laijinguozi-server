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

    code = serializers.CharField(write_only=True)

    def create(self, validated_data):
        js_code = validated_data.pop('code')

        result = wechat_login.code2session(js_code)

        if result.get('errcode') != 0:
            raise serializers.ValidationError('微信获取openid失败')

        wechat_user = WechatUser.objects.filter(openid=result['openid']).first()
        if wechat_user and wechat_user.user:
            # 签发token
            user = wechat_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            validated_data['token'] = token
        if wechat_user and not wechat_user.user:
            validated_data['openid'] = result['openid']     # 严格来说是需要使用session_key加密openid，这里偷懒明文传输
        else:
            WechatUser.objects.create(openid=result['openid'], session_key=result['session_key'])
            validated_data['openid'] = result['openid']
        self.context['view'].validated_data = validated_data
        return wechat_user


class WechatRegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(write_only=True)
    openid = serializers.CharField(write_only=True)

    def create(self, validated_data):
        code = validated_data.pop('code')
        openid = validated_data.pop('openid')
        result = wechat_login.get_phone_number(code)
        if result.get('errcode') != 0:
            raise serializers.ValidationError('微信获取手机号失败。')

        validated_data['mobile'] = result['phone_info']['purePhoneNumber']
        user = super(WechatRegisterSerializer, self).create(validated_data)
        WechatUser.objects.filter(openid=openid).update(user=user)

        # 签发token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        validated_data['token'] = token
        self.context['view'].validated_data = validated_data
        return user

    class Meta:
        model = Users
        fields = ('id', 'nickname', 'avatar', 'code', 'openid')
