from rest_framework.viewsets import ModelViewSet

from core.views import CustomDestroyMessageMixin
from users_app.models import Gender
from users_app.serializers import GenderSerializer


class GenderModelViewSet(ModelViewSet, CustomDestroyMessageMixin):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all()
