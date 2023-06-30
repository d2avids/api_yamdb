from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from reviews.models import CustomUser
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
        user = CustomUser.objects.filter(username=attrs[self.username_field],
                                              confirmation_code=attrs['confirmation_code']).first()
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
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "bio", "role")

    def create(self, validated_data):
        validated_data.pop('password', None)
        return super(CustomUserSerializer, self).create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериалиазтор регистрации по username и email с получением confirmation_code
    на почту, валидация на уникальность и username != me
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    username = serializers.CharField(
        max_length=30,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

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

    def validate(self, attrs):
        data = super().validate(attrs)
        if data['username'] == 'me':
            raise serializers.ValidationError("<me> can't be a username")

        return data
