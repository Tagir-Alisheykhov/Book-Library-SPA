from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer.',
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "A user with that username already exists."
        },
        blank=False
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        """Строковое отображение пользователя"""
        return f"username: {self.username}, email: {self.email}"
