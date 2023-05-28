from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
        validators=[validators.RegexValidator(regex=r'^[\w.@+-]+$')],
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    def __str__(self):
        return self.username


class Follow (models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
