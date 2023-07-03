from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserModelViewSet, TokenObtainView, RegisterModelViewSet, ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register("v1/users", CustomUserModelViewSet, basename="user")

RegisterModelViewSet = RegisterModelViewSet.as_view({
    'post': 'create',
})
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path("", include(router_v1.urls)),
    path("v1/auth/token/", TokenObtainView.as_view(), name="token_obtain"),
    path('v1/auth/signup/', RegisterModelViewSet, name="signup"),
]
