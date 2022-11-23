from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework import status


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
