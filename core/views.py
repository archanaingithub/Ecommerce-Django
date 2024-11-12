from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserActivationSerializer,
)
from django.contrib.auth import get_user_model, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

User = get_user_model()

# Create your views here.


class UserViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserLoginSerializer
        )
    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": serializer.data,
                    "token": token.key,
                }
            )
        return Response(
                {
                    "details: invalid credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserActivationSerializer
        )
    @action(methods=["POST"], detail=False)
    def activation(self, request):
        serializer = UserActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                email=serializer.validated_data["email"],
                otp=serializer.validated_data["otp"],
            )
            user.is_active = True
            user.save()
            return Response(
                {"details": "your account has been activated successfully!"},
                status=status.HTTP_200_OK,
            )
        except user.DoesNotExist:
            return Response(
                {"details": "invalid credentials"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
