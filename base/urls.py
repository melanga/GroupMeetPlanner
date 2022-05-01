from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('group/<int:pk>/', views.group_page, name="group"),
    path('delete-time/<int:pk>', views.delete_time, name="delete-time"),
    path('update-time/<int:pk>', views.update_time, name="update_time"),
    path('login', views.login_page, name="login-page"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register-page"),
    path('create-group', views.group_creation_page, name="create-group"),
    path('update-group/<int:gid>', views.update_group, name="update-group"),
    path('delete-group/<int:pk>', views.delete_group, name="delete-group"),
    path('add-member/<int:uid>/<int:gid>', views.add_member, name="add-member"),
    path('remove-member/<int:uid>/<int:gid>', views.remove_member, name="remove-member"),
    path('leave-group/<int:gid>', views.leave_group, name="leave-group"),
    path('update-user', views.update_user, name="update-user"),

    # Password Reset Auth Urls
    path('password-change/', views.PasswordChange.as_view(), name="password-change"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
