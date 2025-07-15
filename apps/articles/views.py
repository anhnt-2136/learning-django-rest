from rest_framework import viewsets
from rest_framework.response import Response

from apps.articles.models import Article
from apps.articles.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"

    # Override the list method to customize the response format for learning purposes
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "articles": response.data,
            }
        )
