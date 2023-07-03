from  rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView

# from .permissions import (IsAuthorOrReadOnly, IsAdminOrReadOnly,
#                           IsModerator)
from .filters import TitleFilter
from reviews.models import CustomUser, Title, Genre, Category
from .serializers import (CustomTokenObtainSerializer, CustomUserSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer,
                          TitleSafeSerializer)


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # permission_classes = (
    #     IsAuthorOrReadOnly,
    #     IsAdminOrReadOnly,
    #     IsModerator
    # )
    filterset_class = TitleFilter

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
    # permission_classes = (IsAdminOrReadOnly, IsModerator)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Метод исключает запрос отдельного объекта при GET-запросе."""
        raise MethodNotAllowed('GET')


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет предоставляет список типов произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    # permission_classes = (IsAdminOrReadOnly, IsModerator) 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Метод исключает запрос отдельного объекта при GET-запросе."""
        raise MethodNotAllowed('GET')
