from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    User может публиковать отзывы и ставить оценки,
    + изменять свои материалы
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к чтению только для пользователя, а изменение
    или добавление только для администратора
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsModerator(permissions.BasePermission):
    """
    Модератор имеет право удалять и редактировать любые отзывы и комментарии
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    """
    Администратор имеет полные права на управление всем контентом проекта
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
