from rest_framework import serializers

from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "confirm_password",
            "bio",
            "image",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop("confirm_password", None)

        # Create user using the manager's create_user method
        user = User.objects.create_user(**validated_data)  # type: ignore
        return user
