from rest_framework import viewsets

from realworld.mixins import CustomResponseMixin

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
