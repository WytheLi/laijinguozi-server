import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, jwt_decode_handler


class JwtTokenAuthentication(JSONWebTokenAuthentication):
    """
        由于微信登录，不仅要判断请求头中token有效，而且要有open_id。这里对原先的认证类进行重写
    """
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            return False

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)


class AuthBackend(ModelBackend):
    """
        自定义认证后端ModelBackend，完成手机号、邮箱、用户名等多账号登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UsersModel = get_user_model()
        try:
            user = UsersModel.objects.get(
                # username=<account_number> or mobile=<account_number> or email=<account_number>
                Q(username=username) | Q(mobile=username) | Q(email=username)
            )
        except UsersModel.DoesNotExist:
            return None

        # 校验密码
        if user.check_password(password):
            return user


class JwtTokenBlackMiddleware(MiddlewareMixin):
    """
        jwt token黑名单，主动失效（如注销、登出、忘记密码、修改密码、JWT续签等操作）后原先签发的token禁止访问。
    """
    def process_request(self, request):
        authorization = request.headers.get('Authorization')
        if authorization:
            token = authorization.split(' ')[1]
            redis_conn = get_redis_connection('token_blacklist')
            if redis_conn.get(token):
                return HttpResponse('401 Forbidden.', status=status.HTTP_401_UNAUTHORIZED)


