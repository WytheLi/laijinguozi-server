import json
import logging

from rest_framework import status


logger = logging.getLogger('django')


class APIException(Exception):
    """
        API异常基类

        由全局的异常捕获中间件捕获后，给前端友好的响应
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'unknown error.'

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return self.detail


class ParseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptable(APIException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class Throttled(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS




