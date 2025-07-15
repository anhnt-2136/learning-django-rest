from rest_framework import viewsets

from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
