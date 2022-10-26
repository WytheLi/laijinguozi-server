import logging
import traceback

import sentry_sdk
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from sentry_sdk.integrations.django import DjangoIntegration

logger = logging.getLogger('django')


class ViewException(Exception):
    """ 视图异常基类 """


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

        return JsonResponse(data={'code': 500, 'msg': str(exception)}, status=500)
