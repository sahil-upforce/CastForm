import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import BaseModelManager


class BaseModel(models.Model):
    public_id = models.UUIDField(verbose_name=_("public id"), default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(verbose_name=_("deleted at"), null=True, blank=True)
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="users_app.User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        verbose_name=_("updated by"),
        to="users_app.User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="+",
    )
    deleted_by = models.ForeignKey(
        verbose_name=_("deleted by"),
        to="users_app.User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="+",
    )

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()

    @property
    def is_new(self):
        return self._state.adding

    @staticmethod
    def make_slug(input_string: str):
        return input_string.strip().lower().replace(" ", "_")
