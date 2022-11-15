from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('wechat/login', views.WechatLoginView.as_view()),
    path('wechat/register', views.WechatRegisterView.as_view()),
    path('current_user/info', views.UserInfoView.as_view()),
    path('user', views.UserInfoView.as_view()),     # /user?id=1
    path('logout', views.LogoutView.as_view())
]
