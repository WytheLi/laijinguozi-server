import time

from django.forms import model_to_dict
from django_redis import get_redis_connection
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from utils.response import success
from .models import Users
from .serializers import WechatLoginSerializer, UserSerializer, WechatRegisterSerializer, LoginSerializer

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

# Create your views here.


class LoginView(GenericAPIView):
    """
        # 登录并签发token
        # 其中头部信息的组装，token的生成
            rest_framework_jwt.views.ObtainJSONWebToken
            # rest_framework_jwt.utils.jwt_payload_handler
            # rest_framework_jwt.utils.jwt_encode_handler
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token = serializer.validated_data.get('token')

        user_info = model_to_dict(user, fields=['id', 'username', 'mobile', 'email', 'avatar', 'nickname', 'is_employee'])

        data = {
            'user': user_info,
            'token': token
        }
        return success(data)


class WechatLoginView(APIView):
    """
        小程序登录流程：
            1、小程序获取code
            2、将code发送到开发者服务器
            3、开发者服务器请求微信服务器获取openid、session_key
                3.1、若数据库中存在该微信用户&绑定了手机号，签发token
                3.2、若数据库中存在该微信用户，但是未绑定手机号，响应未注册信息，让用户请求注册接口绑定手机号
                3.3、若数据库中不存在该微信用户，创建微信用户记录，响应未注册信息，让用户请求注册接口绑定手机号
        参考：
            - rest_framework.generics.CreateAPIView
            - rest_framework_jwt.views.JSONWebTokenAPIView
    """
    serializer_class = WechatLoginSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            self.__class__.__name__
        )
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())     # 序列化器实例化的时，将request、view实例注入到序列化器中，供序列化器使用
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = self.validated_data.get('token')
        if token:
            return success({'token': token})
        else:
            return success(data={'openid': self.validated_data.get('openid')})


class WechatRegisterView(GenericAPIView):

    serializer_class = WechatRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['token'] = self.validated_data['token']
        return success(data)


class UserInfoView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer

    def get_object(self, pk):
        if not pk:
            # 获取当前登录用户详情
            return self.request.user
        else:
            # 获取指定用户详情
            return Users.objects.get(pk=pk)

    def get_serializer_class(self):
        assert self.serializer_class is not None, ( self.__class__.__name__ )
        return self.serializer_class

    def get_serializer(self, instance):
        serializer_class = self.get_serializer_class()
        return serializer_class(instance)

    def get(self, request, *args, **kwargs):
        uid = request.query_params.get('id')
        instance = self.get_object(uid)
        serializer = self.get_serializer(instance)
        data = serializer.data

        return success(data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
            登出，在redis里面添加token黑名单。实现jwt token主动失效
                key: jwt-token
                expiry: <token有效期>
                value: <失效时间>
        """
        authorization = request.headers.get('Authorization')
        token = authorization.split(' ')[1]
        payload = jwt_decode_handler(token)
        redis_conn = get_redis_connection('token_blacklist')
        redis_conn.setex(token, payload['exp'], time.time())
        return success(msg='logout success.')
