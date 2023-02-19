from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=20,
        null=True,
        blank=True

    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_username_and_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return any(
            (
                self.role == self.ADMIN,
                self.is_superuser,
                self.is_staff,
            )
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
