from django.urls import path
from . import views

urlpatterns = [
    path('carts', views.CartViewSet.as_view({'get': 'list'})),
    # 加购
    path('carts/add', views.CartViewSet.as_view({'post': 'create'})),
]
