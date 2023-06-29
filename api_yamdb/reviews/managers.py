from django.contrib.auth.models import UserManager

from .constants import Role


class CustomUserManager(UserManager):
    def admins(self):
        return self.filter(role=Role.ADMIN)

    def moderators(self):
        return self.filter(role=Role.MODERATOR)

    def users(self):
        return self.filter(role=Role.USER)
