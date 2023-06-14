from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]
    email = models.EmailField(
        verbose_name='Почта',
        unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=8,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
