from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


def validate_not_me(value):
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя.')


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор')
    ]

    role = models.CharField('user role',
                            max_length=9,
                            choices=ROLE_CHOICES,
                            blank=False,
                            default=USER
                            )
    bio = models.TextField('user bio', blank=True)
    confirmation_code = models.CharField('email code',
                                         blank=True, max_length=9)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters, fewer. Letters, digits and @/./+/-/_.'),
        validators=[AbstractUser.username_validator, validate_not_me],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['username', 'email'],
            name='unique_username_email',
        )]

    @property
    def is_admin(self):
        return (self.role == self.ADMIN or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
