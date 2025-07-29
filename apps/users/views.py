from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.mixins import BaseResponseMixin
from apps.users.serializers import UserSerializer, UserUpdateSerializer


class UserViewSet(APIView, BaseResponseMixin):
    """
    Custom API view set for authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return self.response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(UserSerializer(request.user).data)
