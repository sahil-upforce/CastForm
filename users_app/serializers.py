from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from core.async_task import send_mail_to_user
from core.serializers import BaseSerializer
from core.tokens import account_activation_token
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

    def validate_username(self, value):
        if User.all_objects.filter(username=value).first():
            raise serializers.ValidationError("Username is already exists")
        return value

    def validate_email(self, value):
        if User.all_objects.filter(email=value).first():
            raise serializers.ValidationError("Email is already exists")
        return value

    def validate_phone(self, value):
        if value:
            if User.all_objects.filter(phone=value).first():
                raise serializers.ValidationError("Phone Number is already exists")
        return value

    def validate_gender_id(self, value):
        return value.pk

    def validate_user_type_id(self, value):
        return value.pk

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["is_active"] = False
        user = super().create(validated_data)
        current_site = get_current_site(self.context["request"])
        send_mail_to_user.apply_async(
            kwargs={
                "subject": "VERIFY YOUR EMAIL",
                "to": (user.email,),
                "html_template": "emails/user_email_verification.html",
                "context": {
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            }
        )
        return user
