from django.urls import path
from . import views

urlpatterns = [
    # 购物车列表
    path('carts', views.CartViewSet.as_view({'get': 'list'})),
    # 加购
    path('cart/add', views.CartViewSet.as_view({'post': 'create'})),
    # 购物车勾选，计算优惠价，判断是否能下单
    path('cart/checked', views.CartCheckedView.as_view()),
]
