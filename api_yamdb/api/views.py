from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import CustomUser
from rest_framework.filters import SearchFilter

from .serializers import CustomTokenObtainSerializer, CustomUserSerializer, RegisterSerializer


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

    @action(detail=False, methods=["get", "patch"])
    def me(self, request, pk=None):
        if request.method == 'PATCH':
            self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
        self.get_serializer().save()
        return Response(self.get_serializer(request.user).data)


class RegisterModelViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()