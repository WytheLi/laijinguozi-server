from django.urls import path

from apps.users.views import LoginView

urlpatterns = [
    # 手机登录
    path('phone/login', LoginView.as_view()),
    # 微信登录
    # path('wechat/login/', ),
]