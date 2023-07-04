from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import CustomUser, Review, Title
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter

from .permissions import IsAdmin, IsModerator, IsAuthorOrReadOnly
from .serializers import CustomTokenObtainSerializer, CustomUserSerializer, RegisterSerializer, ReviewSerializer, CommentSerializer



class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet для User эндпоинтов с username вместо id и реализованным поиском
    """

    lookup_field = 'username'
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('username,' )
    permission_classes = (IsAdmin, )

    @action(detail=False,
            methods=["get", "patch"],
            permission_classes=(IsAuthorOrReadOnly, )
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
    

class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = [IsAdmin, IsModerator, IsAuthorOrReadOnly]

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
    permission_classes = [IsAdmin, IsModerator, IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
