from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserModelViewSet, TokenObtainView, TitleViewSet,
                    GenreViewSet, CategoryViewSet)

router_v1 = DefaultRouter()
router_v1.register("v1/users", CustomUserModelViewSet, basename="user")
router_v1.register("v1/titles", TitleViewSet, basename="title")
router_v1.register("v1/genres", GenreViewSet, basename="genre")
router_v1.register("v1/categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("v1/auth/token/", TokenObtainView.as_view(), name="token_obtain"),
]
