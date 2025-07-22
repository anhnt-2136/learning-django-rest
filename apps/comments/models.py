from django.db import models

from apps.articles.models import Article
from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin
from apps.users.models import User


class Comment(WithTimestampsMixin, StrReprMixin):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta(WithTimestampsMixin.Meta):
        ordering = ["-id"]
