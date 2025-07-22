from django.db import models

from apps.core.mixins import StrReprMixin


class Tag(models.Model, StrReprMixin):  # noqa: DJ008
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
