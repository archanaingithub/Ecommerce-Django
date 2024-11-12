from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AbstractUser
from random import randint
from rest_framework.authentication import authenticate
from django.core.mail import send_mail

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)
    username = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(max_length=16)
    confirm_password = serializers.CharField(max_length=16, write_only=True)
    """confirm password doesn't exist in database(v_d).
    confirm password would be empty so, we put it as write only field"""

    class Meta:
        model = AbstractUser
        fields = [
            "email",
            "otp",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("user with that email already exists!")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("user with that username already exists!")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "password and confirm password do not match"
            )
        return super().validate(attrs)

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user.otp = randint(0000, 9999)
        user.is_active = False
        user.save()
        subject = "Activation of your account"
        message = f"""
        {user.username} your account has been registered!
        Opt for activating your account is {user.otp}"""

        email_from = "Ecommerce@gmail.com"
        recipient_list = [user.email]

        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)
    password = serializers.CharField(max_length=300, write_only=True)
    
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError("invalid email or password")
        
        attrs["user"] = user
        return attrs
    
    
class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)
    otp = serializers.IntegerField()
    