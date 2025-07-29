from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import CustomModelViewSet

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(CustomModelViewSet):
    """
    A simple ViewSet for viewing and editing articles.
    """

    queryset = (
        Article.objects.all().select_related("author").prefetch_related("tags")
    )
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        queryset = (
            Article.objects.all()
            .select_related("author")
            .prefetch_related("tags")
        )
        author = self.request.GET.get("author")
        if author is not None:
            queryset = queryset.filter(author__username=author)

        tags = self.request.GET.getlist("tags[]")
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset
