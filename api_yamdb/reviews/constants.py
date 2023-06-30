from django.db import models


class Role(models.TextChoices):
    """Пользовательские роли."""

    USER = "USER", "user"
    MODERATOR = "MODERATOR", "moderator"
    ADMIN = "ADMIN", "admin"
