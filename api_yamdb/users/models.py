from django.db import models
from django.contrib.auth.models import AbstractUser
from api_yamdb.settings import CONFIRMATION_CODE_LENGTH


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
        blank=False,
        unique=True
    )
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
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'),
        )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
