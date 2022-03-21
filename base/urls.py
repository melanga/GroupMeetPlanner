from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('group/<int:pk>/', views.group_page, name="group"),
    path('delete-time/<int:pk>', views.delete_time, name="delete-time"),
    path('login', views.login_page, name="login-page"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register-page"),
]
