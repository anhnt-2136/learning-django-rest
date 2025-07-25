from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import CustomReadOnlyModelViewSet
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer


class TagViewSet(CustomReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and editing tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
