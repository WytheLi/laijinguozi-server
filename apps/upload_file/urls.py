from django.urls import path
from . import views

urlpatterns = [
    path('upload_auth', views.upload_auth),
    path('auth_code/get', views.AuthTokenView.as_view()),
]
