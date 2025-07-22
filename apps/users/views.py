from rest_framework import viewsets

from realworld.mixins import CustomResponseMixin

from .models import User
from .serializers import UserSerializer


class UserViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
