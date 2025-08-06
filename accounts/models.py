from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель аккаунта пользователя."""
    pass
