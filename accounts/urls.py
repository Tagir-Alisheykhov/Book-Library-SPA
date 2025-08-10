"""
Конечные точки приложения `accounts`.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView
)

from accounts.apps import AccountsConfig
from . import views


app_name = AccountsConfig.name

urlpatterns = [
    # Регистрация
    path("register/", views.UserCreateAPIView.as_view(), name="user-register"),

    # Аутентификация JWT
    path('token/', TokenObtainPairView.as_view(), name='token-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Управление пользователями (только для админов)
    path('', views.UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),

    # Профиль текущего пользователя
    path('me/', views.UserMeAPIView.as_view(), name='user-me'),
]
