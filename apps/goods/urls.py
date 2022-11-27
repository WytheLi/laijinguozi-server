from django.urls import path
from . import views

urlpatterns = [
    # 物料
    path('materials', views.MaterialViewSet.as_view({'get': 'list'})),
    path('material/create', views.MaterialViewSet.as_view({'post': 'create'})),
    path('material/update/<int:pk>', views.MaterialViewSet.as_view({'patch': 'partial_update'})),
    path('material/get/<int:pk>', views.MaterialViewSet.as_view({'get': 'retrieve'})),
    path('material/delete/<int:pk>', views.MaterialViewSet.as_view({'delete': 'destory'})),

    # 上架商品（勾选物料创建，自定义创建）
    path('goods/create', views.GoodsViewSet.as_view({'post': 'create'})),
    path('goods', views.GoodsViewSet.as_view({'get': 'list'})),
]
