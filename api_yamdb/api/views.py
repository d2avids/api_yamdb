from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import CustomUser, Review, Title
from django.shortcuts import get_object_or_404
from .permissions import IsAdminOrReadOnly, IsModerator

from .serializers import CustomTokenObtainSerializer, CustomUserSerializer, ReviewSerializer, CommentSerializer


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly, IsModerator]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly, IsModerator]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
        