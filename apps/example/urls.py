from django.urls import path
from . import views

urlpatterns = [
    path('person', views.PersonView.as_view()),
]