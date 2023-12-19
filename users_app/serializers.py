from rest_framework import serializers

from core.serializers import BaseSerializer
from users_app.models import Gender


class GenderSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (*BaseSerializer.Meta.fields, "name", "slug")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields, "slug")
