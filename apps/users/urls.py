from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views

from apps.users.views import LoginView, UserInfo

urlpatterns = [
    path('login', views.obtain_auth_token),    # 登录并签发token
    path('jwt_auth', obtain_jwt_token),
    path('user/<int:uid>', UserInfo.as_view()),
    # 微信登录
    # path('wechat/login/', ),
]
