from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import CustomUser

from .serializers import CustomTokenObtainSerializer, CustomUserSerializer


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
