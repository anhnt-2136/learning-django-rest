from django.db import models


class WithTimestampsMixin(models.Model):
    """
    Mixin to add created_at and updated_at fields to a model.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
