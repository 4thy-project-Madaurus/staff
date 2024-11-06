from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

from utils.models import  UUIDModel

class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('User must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) 

        return self.create_user(email, password, **extra_fields)
    


choices = (
    ('admin', 'admin'),
    ('teacher', 'teacher'),
    ('student', 'student'),
)
class User(AbstractUser, PermissionsMixin, UUIDModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

class Admin(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    otp = models.CharField(max_length=6, blank=True, null=True)
    
class OTP(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)