from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.articles.models import Article
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.core.mixins import CustomModelViewSet


class CommentViewSet(CustomModelViewSet):
    """
    A simple ViewSet for viewing and editing comments.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        return Comment.objects.filter(
            article__slug=self.kwargs["article_slug"]
        ).select_related("owner")

    def perform_create(self, serializer):
        article_slug = self.kwargs.get("article_slug")
        article = get_object_or_404(Article, slug=article_slug)
        serializer.save(article=article, owner=self.request.user)
