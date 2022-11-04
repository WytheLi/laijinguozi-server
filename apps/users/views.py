from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken

from utils.response import success
from .models import Users
from .serializers import WechatLoginSerializer, UserSerializer


# Create your views here.


class LoginView(ObtainJSONWebToken):
    """
        # 登录并签发token
        # 其中头部信息的组装，token的生成
            # rest_framework_jwt.utils.jwt_payload_handler
            # rest_framework_jwt.utils.jwt_encode_handler
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
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
            3、开发者服务器通过微信接口服务校验登录凭证
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
        if serializer.is_valid():
            serializer.save()
            return success({'token': self.token})


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

    def get(self, request, uid):
        request.headers
        instance = self.get_object(uid)
        serializer = self.get_serializer(instance)
        data = serializer.data

        return success(data)

