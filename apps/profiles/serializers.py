from rest_framework import serializers

from apps.users.models import User, UserFollowing


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "image", "following"]

    def get_following(self, obj):
        """
        Check if current user is following this profile user.
        """
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return UserFollowing.objects.filter(
            user=request.user, following_user=obj
        ).exists()


class UserFollowingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    following_user = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ["user", "following_user"]

    def validate(self, attrs):
        """
        Check if user has already followed this user.
        """
        request = self.context.get("request")
        user = request.user if request else None
        following_user = self.context.get("following_user")

        if user == following_user:
            raise serializers.ValidationError("You cannot follow yourself.")

        # Check for existing follow
        if UserFollowing.objects.filter(
            user=user, following_user=following_user
        ).exists():
            raise serializers.ValidationError(
                "You are already following this user."
            )

        return attrs

    def get_user(self, obj):
        """
        Return the username of the user who is following.
        """
        return obj.user.username if obj.user else None

    def get_following_user(self, obj):
        """
        Return the username of the user being followed.
        """
        return obj.following_user.username if obj.following_user else None
