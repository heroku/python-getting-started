"""All application models."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Public user model."""

    avatar = models.ImageField(upload_to=None, verbose_name='аватарка')
    first_name = models.CharField(max_length=64, verbose_name='имя')
    last_name = models.CharField(max_length=64, verbose_name='фамилия')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
