from datetime import datetime, timedelta

from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class LoginView(View):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return HttpResponse({"code": 0,
                                "msg": "用户名或密码不对!"})
        # 删除原有的Token
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        # 创建新的Token
        token = Token.objects.create(user=user)
        return JsonResponse({"code": 0,
                             "msg": "login success!",
                             "username": user.username,
                             "token": token.key})


class UserInfo(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, uid):
        from apps.users.models import Users
        user = Users.objects.get(pk=uid)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})

