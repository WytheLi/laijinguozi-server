from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginView(View):

    def post(self, request):
        division_by_zero = 1 / 0
        return JsonResponse({'code': 200, 'msg': "请求成功"})
