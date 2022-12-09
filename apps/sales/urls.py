from django.urls import path

from . import views

urlpatterns = [
    # 提交订单
    path('order/create', views.OrderViewSet.as_view({'post': 'create'})),
    # 订单列表
    path('orders', views.OrderViewSet.as_view({'get': 'list'})),
    # 订单明细
    path('order/<int:pk>', views.OrderViewSet.as_view({'get': 'get'})),
    # 取消订单
    path('order/cancel/<int:pk>', views.OrderCancelView.as_view()),
    # 支付订单
    path('order/payment/<int:pk>', views.OrderPaymentView.as_view()),
    # 支付回调地址
    path('order/payment/callback/<str:bill_number>', views.OrderPaymentView.as_view()),
]
