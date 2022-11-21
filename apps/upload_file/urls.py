from django.urls import path
from . import views

urlpatterns = [
    path('upload_auth', views.UploadAuthView.as_view()),
    path('auth_code/get', views.AuthTokenView.as_view()),
]
