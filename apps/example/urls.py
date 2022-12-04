from django.urls import path
from . import views

urlpatterns = [
    path('person', views.PersonView.as_view()),
    path('group/members', views.GroupView.as_view()),
    path('task_mul', views.task_add),
]
