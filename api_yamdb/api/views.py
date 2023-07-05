from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets, filters, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .filters import TitleFilter
from reviews.models import CustomUser, Title, Genre, Category, Review
from .serializers import (CustomTokenObtainSerializer, CustomUserSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer,
                          TitleSafeSerializer, RegisterSerializer,
                          ReviewSerializer,
                          CommentSerializer, CustomUserMeSerializer)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdmin, IsAdmin


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet для User эндпоинтов с username вместо id и реализованным поиском
    """
    lookup_field = 'username'
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdmin,)
    pagination_class = PageNumberPagination

    @action(detail=False,
            methods=["get", "patch"],
            permission_classes=(IsAuthenticated,),
            serializer_class=CustomUserMeSerializer
            )
    def me(self, request, pk=None):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(self.get_serializer(request.user).data)


class RegisterModelViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        """Стандартный метод вьюсет, который определяет
        какой из доступных сериализаторов должен обрабатывать
        данные в зависимости от действия."""
        if self.action == ['list', 'retrieve']:
            return TitleSafeSerializer
        return TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        """Метод исключает запрос отдельного объекта при GET-запросе."""
        raise MethodNotAllowed('GET')


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список типов произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Метод исключает запрос отдельного объекта при GET-запросе."""
        raise MethodNotAllowed('GET')


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdmin, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdmin, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
