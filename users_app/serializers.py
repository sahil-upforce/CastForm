from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.serializers import BaseSerializer
from users_app.models import Gender, UserType

User = get_user_model()


class GenderSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (*BaseSerializer.Meta.fields, "name", "slug")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields, "slug")


class UserTypeSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = (*BaseSerializer.Meta.fields, "name", "slug")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields, "slug")


class UserSerializer(BaseSerializer, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    gender = GenderSerializer(read_only=True)
    user_type = UserTypeSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            *BaseSerializer.Meta.fields,
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "phone",
            "gender",
            "user_type",
        )
        read_only_fields = (*BaseSerializer.Meta.fields,)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserCreateSerializer(UserSerializer):
    gender_id = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all(), required=True)
    user_type_id = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all(), required=True)

    class Meta:
        model = User
        fields = (
            *BaseSerializer.Meta.fields,
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "phone",
            "gender_id",
            "user_type_id",
        )
        read_only_fields = (*BaseSerializer.Meta.fields,)
        extra_kwargs = {i: {"required": True} for i in fields}

    def validate_phone(self, value):
        if value:
            if User.objects.filter(phone=value).first():
                raise serializers.ValidationError("Phone Number is already exists")
        return value

    def validate_gender_id(self, value):
        return value.pk

    def validate_user_type_id(self, value):
        return value.pk
