from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.mixins import BaseResponseMixin
from apps.registration.serializers import UserRegistrationSerializer
from apps.users.serializers import UserSerializer


class UserRegistrationViewSet(APIView, BaseResponseMixin):
    """
    API endpoint for user authentication and registration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user account.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if isinstance(user, list):
                user = user[0]

            # Generate JWT tokens for the new user
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            # Return user data with tokens
            user_serializer = UserSerializer(user)
            return self.response(
                {
                    "user": user_serializer.data,
                    "tokens": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return self.response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
