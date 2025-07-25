from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from apps.core.mixins import StrReprMixin
from apps.core.models import WithTimestampsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(WithTimestampsMixin, StrReprMixin, AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)
    last_login = None

    strrepr_exclude_fields = ["password"]

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta(WithTimestampsMixin.Meta):
        ordering = ["-id"]
