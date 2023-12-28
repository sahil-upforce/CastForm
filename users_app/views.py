from django.contrib.auth import get_user_model

from core.views import CustomModelViewSet, CustomUserModelViewSet
from users_app import serializers
from users_app.models import Gender, UserType

User = get_user_model()


class GenderModelViewSet(CustomModelViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()


class UserTypeModelViewSet(CustomModelViewSet):
    serializer_class = serializers.UserTypeSerializer
    queryset = UserType.objects.all()


class UserModelViewSet(CustomUserModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        return super().get_serializer_class()
