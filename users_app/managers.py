from django.contrib.auth.models import UserManager

from core.managers import BaseModelManager


class CustomUserManager(UserManager, BaseModelManager):
    def get_queryset(self):
        if self.alive_only:
            return super(CustomUserManager, self).get_queryset().filter(is_active=True)
        return super(CustomUserManager, self).get_queryset()
