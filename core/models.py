from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

# Custom manager for User model to define methods
# for creating and managing user objects
class UserManager(BaseUserManager):
  def create_user(self, username, email, password=None, **extra_fields):
    if username is None:
      raise TypeError('User should have a username')
    if email is None:
      raise TypeError('User should have an email')

    user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save()
    return user
    
  def create_superuser(self, username, email, password=None):
    if password is None:
      raise TypeError('Password should not be None')

    user = self.create_user(username, email, password)
    user.is_superuser=True
    user.is_staff=True
    user.save()
    return user

AUTH_PROVIDERS = { 'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=255, unique=True, db_index=True)
  first_name = models.CharField(max_length=255, db_index=True)
  last_name = models.CharField(max_length=255, db_index=True)
  email = models.EmailField(max_length=255, unique=True, db_index=True)
  is_verified = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  # for logging
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  # manage object of User with UserManager
  objects=UserManager()
  
  def __str__(self):
    return self.first_name + " " + self.last_name
  
  def tokens(self):
    refresh = RefreshToken.for_user(self)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token)
    }
