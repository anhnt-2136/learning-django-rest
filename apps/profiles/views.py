from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.core.mixins import BaseResponseMixin
from apps.profiles.serializers import ProfileSerializer
from apps.users.models import User, UserFollowing


class ProfileViewSet(GenericViewSet, BaseResponseMixin):
    """
    ViewSet for user profiles and following functionality.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def retrieve(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(user, context={"request": request})
        return self.response(serializer.data)

    @action(detail=True, methods=["get", "post", "delete"])
    def follow(self, request, username=None):
        if request.method == "POST":
            return self._follow_user(request, username)
        elif request.method == "DELETE":
            return self._unfollow_user(request, username)

    def _follow_user(self, request, username):
        following_user = get_object_or_404(User, username=username)

        if request.user == following_user:
            raise ValidationError("You cannot follow yourself.")

        if UserFollowing.objects.filter(
            user=request.user, following_user=following_user
        ).exists():
            raise ValidationError("You are already following this user.")

        UserFollowing.objects.create(
            user=request.user, following_user=following_user
        )

        return self.response(status=status.HTTP_201_CREATED)

    def _unfollow_user(self, request, username):
        following_user = get_object_or_404(User, username=username)

        try:
            follow_relationship = UserFollowing.objects.get(
                user=request.user, following_user=following_user
            )
            follow_relationship.delete()

            return self.response(status=status.HTTP_204_NO_CONTENT)

        except UserFollowing.DoesNotExist:
            raise ValidationError("You are not following this user.") from None
