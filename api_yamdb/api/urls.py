from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserModelViewSet, TokenObtainView, RegisterModelViewSet,
                    TitleViewSet, GenreViewSet, CategoryViewSet,
                    ReviewViewSet, CommentViewSet)

router_v1 = DefaultRouter()
router_v1.register("users", CustomUserModelViewSet, basename="user")
router_v1.register("titles", TitleViewSet, basename="title")
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register('titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register('titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   '/comments', CommentViewSet, basename='comments')

RegisterModelViewSet = RegisterModelViewSet.as_view({
    'post': 'create',
})

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/token/", TokenObtainView.as_view(), name="token_obtain"),
    path('auth/signup/', RegisterModelViewSet, name="signup"),
]
