from django.db import models

from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin


class ArticleFavorite(WithTimestampsMixin, StrReprMixin):
    """
    Model representing a user's favorite article.
    """

    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    class Meta(WithTimestampsMixin.Meta):
        unique_together = ("article", "user")
        ordering = ["-id"]
