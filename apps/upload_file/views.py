import uuid

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.response import success

# Create your views here.


class UploadAuthView(APIView):
    """
        go-fastdfs文件上传认证
        https://sjqzhang.github.io/go-fastdfs/authentication.html#custom
    """
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        redis_conn = get_redis_connection('valid_auth')
        if redis_conn.get(code):
            return "ok"
        else:
            return "fail"


class AuthTokenView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        code = str(uuid.uuid4()).replace('-', '')

        redis_conn = get_redis_connection('valid_auth')
        redis_conn.setex(code, 60 * 5, request.user.id)
        return success({"code": code})

