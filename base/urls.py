from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('group/<int:pk>/', views.group_page, name="group"),
]
