from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import CustomUser, Title, Category, Genre, Review, Comment
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from reviews.utils import Util
from django.utils import timezone


class CustomTokenObtainSerializer(TokenObtainSerializer):
    """Получение токена по username и confirmation_code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        self.fields.pop('password', None)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = CustomUser.objects.filter(
            username=attrs[self.username_field],
            confirmation_code=attrs['confirmation_code']
        ).first()
        if not user:
            raise exceptions.AuthenticationFailed(
                "Incorrect username or confirmation_code",
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        self.user = user

        user.last_login = timezone.now()
        user.save()

        return {'token': str(self.get_token(self.user).access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомного юзера, исключение пароля."""
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()),
                    RegexValidator(
                        regex=r'^[\w.@+-]+$',
                        message='Имя пользователя может содержать '
                                'только буквы, цифры и следующие символы: '
                                '@/./+/-/_'
                    )]
    )

    class Meta:
        model = CustomUser
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def create(self, validated_data):
        validated_data.pop('password', None)
        return super(CustomUserSerializer, self).create(validated_data)

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'username' in data:
            if data['username'] == 'me':
                raise serializers.ValidationError("<me> can't be a username")

        return data


class CustomUserMeSerializer(CustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "bio", "role",)
        read_only_fields = ("role",)


class RegisterSerializer(CustomUserSerializer):
    """
    Сериалиазтор регистрации по username и email с получением confirmation_code
    на почту, валидация на уникальность и username != me
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.save()

        Util.send_mail(
            validated_data['email'],
            user.confirmation_code
        )

        return user


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений при безопасных запросах."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений при небезопасных запросах."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Comment'''
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для для модели Review'''
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')
