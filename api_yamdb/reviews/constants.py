from django.db import models


class Role(models.TextChoices):
    """Пользовательские роли."""
    USER = 'USER', 'User'
    MODERATOR = 'MODERATOR', 'Moderator'
    ADMIN = 'ADMIN', 'Administrator'