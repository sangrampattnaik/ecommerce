import datetime
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from ecommerce.utils import BaseModel



class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    mobile = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Owner and Customer
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default="Male")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    def _str_(self):
        return self.email

    objects = CustomUserManager()

    class Meta:
        db_table = "users"  # Table Name