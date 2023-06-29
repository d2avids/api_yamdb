from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import Role


class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    bio = models.CharField(max_length=500, blank=True, null=True)

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff

    def __str__(self) -> str:
        return self.username
