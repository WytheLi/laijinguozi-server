import uuid

from django.shortcuts import render
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.response import success

# Create your views here.


class UploadAuthView(APIView):

    def post(self, request, *args, **kwargs):
        """
            go-fastdfs文件上传认证
            https://sjqzhang.github.io/go-fastdfs/authentication.html#custom

            在go-fastdfs配置文件中配置`auth_url`，/file_service/upload_auth。
            前端会携带`auth_token`凭证请求是否允许上传文件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        code = request.data.get('auth_token')
        redis_conn = get_redis_connection('valid_auth')
        if redis_conn.get(code):
            redis_conn.delete(code)
            return HttpResponse("ok")
        else:
            return HttpResponse("fail")


class AuthTokenView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        code = str(uuid.uuid4()).replace('-', '')

        redis_conn = get_redis_connection('valid_auth')
        redis_conn.setex(code, 60 * 30, request.user.id)
        return success({"code": code})

