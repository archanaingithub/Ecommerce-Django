from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.IntegerField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="users_in_group", blank=True)

    user_permissions = models.ManyToManyField(
        Permission, related_name="users_with_permission", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
