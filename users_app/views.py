from rest_framework.viewsets import ModelViewSet

from core.views import CustomDestroyMessageMixin
from users_app.models import Gender, UserType
from users_app.serializers import GenderSerializer, UserTypeSerializer


class GenderModelViewSet(ModelViewSet, CustomDestroyMessageMixin):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all()


class UserTypeModelViewSet(ModelViewSet, CustomDestroyMessageMixin):
    serializer_class = UserTypeSerializer
    queryset = UserType.objects.all()
