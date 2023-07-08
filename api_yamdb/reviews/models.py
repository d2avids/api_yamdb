import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone

from api_yamdb.settings import SLUG_REGEX
from .constants import Role


class CustomUser(AbstractUser):
    """Кастомный юзер с пользовательской ролью .constants.Role."""
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=50,
        choices=Role.choices,
        default=Role.USER
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True
    )
    bio = models.CharField(
        verbose_name='О себе', max_length=500, blank=True
    )
    confirmation_code = models.UUIDField(
        verbose_name='Код подтверждения', default=str(uuid.uuid4())
    )

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Genre(models.Model):
    """Жанр для произведения: название и slug."""

    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(
        unique=True,
        validators=(
            RegexValidator(
                regex=SLUG_REGEX,
                message="Слаг для страницы с жанром может содержать только "
                "латинские буквы и любые цифры, а также дефис и нижнее "
                "подчеркивание",
            ),
        ),
        verbose_name="Адрес для страницы с жанром",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория для произведения: название и slug."""

    name = models.CharField(max_length=256, verbose_name="Название категории")
    slug = models.SlugField(
        unique=True,
        validators=(
            RegexValidator(
                regex=SLUG_REGEX,
                message="Слаг для страницы с жанром может содержать только "
                "латинские буквы и любые цифры, а также дефис и нижнее "
                "подчеркивание",
            ),
        ),
        verbose_name="Адрес для страницы с категорией",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение: название, год выпуска, описание, категория и жанр."""

    name = models.CharField(
        max_length=256, verbose_name="Название произведения"
    )
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(
                int(timezone.now().year),
                message="Год выпуска для изданных произведений не "
                        "может быть в будущем",
            ),
        ),
        verbose_name="Год выпуска произведения",
    )
    description = models.TextField(
        blank=True, verbose_name="Описание произведения"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Тип произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр произведения'
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная таблица, связывающая жанры с произведениями."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр произведения'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'
            ),
        )
        verbose_name = 'Связь жанра с произведением'
        verbose_name_plural = 'Связь жанров с произведениями'

    def __str__(self):
        return f'Жанр {self.title} - {self.genre}.'


class Review(models.Model):
    """Отзыв пользователя о произведении с возможностью оценки от 1 до 10."""

    title = models.ForeignKey(
        Title,
        verbose_name="Название произведения",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, "Допустимы значения от 1 до 10"),
            MaxValueValidator(10, "Допустимы значения от 1 до 10"),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("pub_date",)
        constraints = (
            models.UniqueConstraint(fields=["title", "author"],
                                    name="unique_review"),
        )


class Comment(models.Model):
    """Комментарий пользователя к отзыву."""

    review = models.ForeignKey(
        Review,
        verbose_name="Отзыв",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор комментария",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("pub_date",)
