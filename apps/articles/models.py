from django.db import models
from slugify import slugify

from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin
from apps.tags.models import Tag
from apps.users.models import User


class Article(WithTimestampsMixin, StrReprMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    tags = models.ManyToManyField(Tag, related_name="articles")

    class Meta(WithTimestampsMixin.Meta):
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
