"""
Настройка админ панели для приложения `accounts`.
"""
from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Управление пользователями в админке"""

    list_display = ["email", "username"]
    list_filter = ["email"]
    search_fields = ["email", "username"]

