from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from users_app.managers import CustomUserManager


class Gender(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=150)
    slug = models.SlugField(verbose_name=_("slug"), max_length=200)

    class Meta:
        verbose_name = "gender"
        verbose_name_plural = "genders"

    def __str__(self):
        return self.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.name = self.name.strip().title()
        self.slug = self.make_slug(self.name)
        super(Gender, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class UserType(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=150)
    slug = models.SlugField(verbose_name=_("slug"), max_length=200)

    class Meta:
        verbose_name = "user type"
        verbose_name_plural = "user types"

    def __str__(self):
        return self.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.name = self.name.strip().title()
        self.slug = self.make_slug(self.name)
        super(UserType, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class User(AbstractUser, BaseModel):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    date_joined = None
    first_name = models.CharField(_("first name"), max_length=150, null=True)
    last_name = models.CharField(_("last name"), max_length=150, null=True)
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    phone = models.CharField(
        verbose_name=_("phone"),
        max_length=16,
        null=True,
        validators=[phoneNumberRegex],
    )
    user_type = models.ForeignKey(
        verbose_name=_("user type"),
        to=UserType,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )
    gender = models.ForeignKey(
        verbose_name=_("gender"),
        to=Gender,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )

    objects = CustomUserManager()
    all_objects = CustomUserManager(alive_only=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username
