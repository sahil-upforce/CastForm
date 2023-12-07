from django.contrib import admin
from django.contrib.auth import get_user_model

from core.admin import BaseAdmin
from users_app.models import Gender, UserType

User = get_user_model()


@admin.register(Gender)
class GenderAdmin(BaseAdmin):
    def get_exclude(self, request, obj=None):
        return tuple(super(GenderAdmin, self).get_exclude(request, obj=None)) + ("slug",)


@admin.register(UserType)
class UserTypeAdmin(BaseAdmin):
    def get_exclude(self, request, obj=None):
        return tuple(super(UserTypeAdmin, self).get_exclude(request, obj=None)) + ("slug",)


@admin.register(User)
class UserAdmin(BaseAdmin):
    pass
