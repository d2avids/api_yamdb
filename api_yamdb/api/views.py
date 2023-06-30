from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import CustomUser, Title, Genre, Category

from .serializers import (CustomTokenObtainSerializer, CustomUserSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer)


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = 
    # filter_backends = (DjangoFilterBackend,) нужен filterset_class
    # filterset_fields = ('name', 'year', 'genre', 'category')


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список типов произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
