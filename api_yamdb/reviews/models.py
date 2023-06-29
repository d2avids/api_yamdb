from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    pass

    def __str__(self) -> str:
        return self.username


class Genre(models.Model):
    """Модель для жанра."""
    pass


class Category(models.Model):
    """Модель для категории(типа)."""
    pass


class Title(models.Model):
    """Модель для произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(
                int(timezone.now().year),
                message='Год выпуска для изданных произведений не может быть в будущем'
            ),
        ),
        verbose_name='Год выпуска произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Тип произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        # through='GenreTitle',
        # through_fields=('genre', 'title'),
        related_name='titles',
        verbose_name='Жанр произведения'
    )


    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


# class GenreTitle(models.Model):
#     """Модель, связывающая жанры с произведениями."""

#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.CASCADE,
#         verbose_name='Жанр произведения'
#     )
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE,
#         verbose_name='Произведение'
#     )
