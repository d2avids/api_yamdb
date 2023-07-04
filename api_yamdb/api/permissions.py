from rest_framework import permissions


class IsAuthorModeratorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        def has_object_permission(self, request, view, obj):
            return (
                    request.method in permissions.SAFE_METHODS
                    or obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin
            )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к чтению только для пользователя, а изменение
    или добавление только для администратора
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin if request.user.is_authenticated else False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin