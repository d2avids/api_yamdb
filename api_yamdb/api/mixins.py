from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet


class PatchModelMixin(mixins.UpdateModelMixin):
    @swagger_auto_schema(auto_schema=None)
    def update(self, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Используйте PATCH-метод")

    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs, partial=True)


class GetCreatePatchDestroyMixin(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    PatchModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass


class ListCreateDestroyMixin(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass
