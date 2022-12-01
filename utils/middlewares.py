import traceback

import sentry_sdk
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework import status
from sentry_sdk.integrations.django import DjangoIntegration

from utils import error_message


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


class ExceptionMiddleware(MiddlewareMixin):

    @staticmethod
    def process_exception(request, exception):
        """
            异常处理, 在views.py中出现异常时被调用，返回None或时HttpResponse对象。 注意：404错误属于url的异常，这里不能被捕捉到。
            例子：可以在视图中触发除0错误
        """
        traceback.print_exc()  # 捕获的错误打印到控制台，方便调试

        if settings.SENTRY_DSN:
            sentry_sdk.init(
                dsn=settings.SENTRY_DSN,
                integrations=[DjangoIntegration()],
                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                # We recommend adjusting this value in production.
                traces_sample_rate=1.0
            )
            sentry_sdk.capture_exception(exception)

        code, message = error_message.UNKNOWN_ERROR
        return JsonResponse(data={'code': code, 'msg': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
