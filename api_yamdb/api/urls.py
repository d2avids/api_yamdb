from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CustomUserModelViewSet,
    GenreViewSet,
    RegisterModelViewSet,
    ReviewViewSet,
    TitleViewSet,
    TokenObtainView,
)

router_v1 = DefaultRouter()
router_v1.register("users", CustomUserModelViewSet, basename="user")
router_v1.register(r"titles", TitleViewSet, basename="title")
router_v1.register(r"genres", GenreViewSet, basename="genre")
router_v1.register(r"categories", CategoryViewSet, basename="category")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)" r"/comments",
    CommentViewSet,
    basename="comments",
)

RegisterModelViewSet = RegisterModelViewSet.as_view(
    {
        "post": "create",
    }
)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/token/", TokenObtainView.as_view(), name="token_obtain"),
    path("auth/signup/", RegisterModelViewSet, name="signup"),
]
