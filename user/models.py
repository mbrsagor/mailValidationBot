from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager
from utils.enum_utils import UserRole, Gender


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class User(AbstractBaseUser, Timestamp, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    role = models.IntegerField(choices=UserRole.get_choices(), default=UserRole.AUTHOR.value)

    # Additional fields for user management
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone']

    def __str__(self):
        return self.email

    @property
    def role_name(self):
        return UserRole(self.role).name

