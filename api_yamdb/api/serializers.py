from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title
from reviews.utils import Util

from api_yamdb.settings import USERNAME_REGEX


class CustomTokenObtainSerializer(TokenObtainSerializer):
    """Получение токена по username и confirmation_code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()
        self.fields.pop("password", None)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = CustomUser.objects.filter(
            username=attrs[self.username_field],
        ).first()

        if not user:
            raise NotFound(
                {"username": "Пользователь с таким username не существует"},
                code="user_not_found",
            )

        if not user.is_active:
            raise ValidationError(
                "Данный аккаунт неактивен",
                code="inactive_account",
            )

        if str(user.confirmation_code) != attrs["confirmation_code"]:
            raise ValidationError(
                {"confirmation_code": "Неверный код подтверждения"},
                code="invalid_confirmation_code",
            )

        self.user = user

        user.last_login = timezone.now()
        user.save()
        return {"token": str(self.get_token(self.user).access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомного юзера, исключение пароля."""

    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            RegexValidator(
                regex=USERNAME_REGEX,
                message="Имя пользователя может содержать "
                "только буквы, цифры и следующие символы: "
                "@/./+/-/_",
            ),
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        if "username" in data:
            if data["username"].lower() == "me":
                raise serializers.ValidationError("<me> can't be a username")

        return data


class CustomUserMeSerializer(CustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class RegisterSerializer(CustomUserSerializer):
    """
    Сериалиазтор регистрации по username и email с получением confirmation_code
    на почту, валидация на уникальность и username != me
    """

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Имя пользователя может содержать "
                "только буквы, цифры и следующие символы: "
                "@/./+/-/_",
            )
        ],
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]

        user = CustomUser.objects.filter(email=email,
                                         username=username).first()
        if user:
            return user

        user = CustomUser.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError("Данный email уже занят")

        user = CustomUser.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError("Данный nickname уже занят")

        user = CustomUser.objects.create(username=username, email=email)

        Util.send_mail(validated_data["email"], user.confirmation_code)

        return user


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ("name", "slug")
        model = Category
        lookup_field = "name"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "name"


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений при безопасных запросах."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id", "name", "year", "description", "genre", "category", "rating",
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений при небезопасных запросах."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title

    def to_representation(self, title):
        """Определяет сериализатор для чтения."""
        serializer = TitleSafeSerializer(title)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""

    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    "Вы не можете добавить более "
                    "одного отзыва на произведение"
                )
        return data

    class Meta:
        model = Review
        fields = ("id", "author", "text", "score", "pub_date")
