from django.db import models


class Role(models.TextChoices):
    """Пользовательские роли."""

    USER = "user", "user"
    MODERATOR = "moderator", "moderator"
    ADMIN = "admin", "admin"
