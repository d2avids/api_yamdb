from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
import uuid

from .constants import Role


class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=Role.choices,
                            default=Role.USER)
    bio = models.CharField(max_length=500, blank=True, null=True)
    confirmation_code = models.UUIDField(default=uuid.uuid4)

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff

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

class Review(models.Model):
    """Модель отзыва пользователя о произведении."""
    title = models.ForeignKey(
        Title,
        verbose_name='Название произведения',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Модель коменнтария пользователя к отзыву."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
