from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.mixins import BaseResponseMixin
from apps.users.models import UserFollowing
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


class UserFollowingView(APIView, BaseResponseMixin):
    """
    API view to get current user's following list.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/user/following
        Get list of users that the current user is following.
        """
        following_relationships = UserFollowing.objects.filter(
            user=request.user
        ).select_related("following_user")

        following_users = []
        for rel in following_relationships:
            user_data = {
                "username": rel.following_user.username,
                "email": rel.following_user.email,
                "bio": rel.following_user.bio,
                "image": rel.following_user.image,
            }
            following_users.append(user_data)

        return self.response(following_users)
