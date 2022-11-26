from django.urls import path
from . import views

urlpatterns = [
    # 物料
    path('materials', views.MaterialViewSet.as_view({'get': 'list'})),
    path('material/create', views.MaterialViewSet.as_view({'post': 'create'})),
    path('material/update/<int:pk>', views.MaterialViewSet.as_view({'patch': 'partial_update'})),
    path('material/get/<int:pk>', views.MaterialViewSet.as_view({'get': 'retrieve'})),
    path('material/delete/<int:pk>', views.MaterialViewSet.as_view({'delete': 'destory'}))
]
