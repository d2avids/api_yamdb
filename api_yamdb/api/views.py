from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, CustomUser, Genre, Review, Title

from .filters import TitleFilter
from .mixins import GetCreatePatchDestroyMixin, ListCreateDestroyMixin
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomTokenObtainSerializer, CustomUserMeSerializer,
                          CustomUserSerializer, GenreSerializer,
                          RegisterSerializer, ReviewSerializer,
                          TitleSafeSerializer, TitleSerializer)


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(GetCreatePatchDestroyMixin):
    """
    ViewSet для User эндпоинтов с username вместо id и реализованным поиском
    """

    lookup_field = "username"
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=(IsAuthenticated,),
        serializer_class=CustomUserMeSerializer,
    )
    def me(self, request, pk=None):
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
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


class TitleViewSet(GetCreatePatchDestroyMixin):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        """Стандартный метод вьюсет, который определяет
        какой из доступных сериализаторов должен обрабатывать
        данные в зависимости от действия."""
        if self.action == ["list", "retrieve"]:
            return TitleSafeSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = PageNumberPagination


class CategoryViewSet(ListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class ReviewViewSet(GetCreatePatchDestroyMixin):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorAdmin,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(GetCreatePatchDestroyMixin):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdmin,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
