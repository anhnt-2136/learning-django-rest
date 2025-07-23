from django.db import models

from apps.articles.models import Article
from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin
from apps.users.models import User


class Comment(WithTimestampsMixin, StrReprMixin):
    content = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta(WithTimestampsMixin.Meta):
        ordering = ["-id"]
