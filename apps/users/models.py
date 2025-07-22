from django.db import models

from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin


class User(WithTimestampsMixin, StrReprMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)

    strrepr_exclude_fields = ["password"]

    class Meta(WithTimestampsMixin.Meta):
        ordering = ["-id"]
