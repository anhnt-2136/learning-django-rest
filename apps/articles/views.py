from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import CustomModelViewSet

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(CustomModelViewSet):
    """
    A simple ViewSet for viewing and editing articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]
