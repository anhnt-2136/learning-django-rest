from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.mixins import CustomModelViewSet

from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer


class UserViewSet(CustomModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=UserRegistrationSerializer,
    )
    def register(self, request):
        """
        Register a new user account.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if isinstance(user, list):
                user = user[0]

            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return user data with tokens
            user_serializer = UserSerializer(user)
            return self.response(
                {
                    "user": user_serializer.data,
                    "tokens": {
                        "access": str(access_token),
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
