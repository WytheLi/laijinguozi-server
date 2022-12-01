from django.urls import path

from . import views

urlpatterns = [
    # 提交订单
    path('orders/create', views.OrderViewSet.as_view({'post': 'create'})),

]
