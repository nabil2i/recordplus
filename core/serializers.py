from rest_framework import serializers
# from .models import User
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = auth.get_user_model()

# WITH DJOSER
class UserCreateSerializer(UserCreateSerializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True)
  
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = [ 'username', 'first_name', 'last_name', 'email', 'password']
    


# WITHOUT DJOSER
class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True)
  
  class Meta:
    model = User
    fields = [ 'username', 'email', 'password']
  
  def validate(self, attrs):
    email = attrs.get('email', '')
    username = attrs.get('username', '')
    
    if not username.isalnum():
      raise serializers.ValidationError('The username should only contain alphanumeric characters.')
    return attrs
  
  def create(self, validated_data):
    return User.objects.create_user(**validated_data)
  

class EmailVerificationSerializer(serializers.ModelSerializer):
  token = serializers.CharField(max_length=555)
  
  class Meta:
    model = User
    fields = ['token']
    
class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=3)
  password = serializers.CharField(max_length=68, min_length=6, write_only=True)
  username = serializers.CharField(max_length=68, min_length=6, read_only=True)
  # tokens = serializers.CharField(max_length=555, min_length=6, read_only=True)
  tokens = serializers.SerializerMethodField()
  
  def get_tokens(self, obj):
    user = User.objects.get(email=obj['email'])
    
    return {
      'access': user.tokens()['access'],
      'refresh': user.tokens()['refresh']
    }
    
  class Meta:
    model = User
    fields = ['email', 'password', 'username', 'tokens']
    
  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')
    filtered_user = User.objects.filter(email=email)
    
    if filtered_user.exists() and filtered_user[0].auth_provider != 'email':
      raise AuthenticationFailed(detail="Please login using " + filtered_user[0].auth_provider)
    
    ## debugging
    # import pdb
    # pdb.set_trace()
    
    user = auth.authenticate(email=email, password=password)
    if not user:
      raise AuthenticationFailed('Invalid credentials.')
    
    if not user.is_active:
      raise AuthenticationFailed('Account disabled, contact admin.')
    
    if not user.is_verified:
      raise AuthenticationFailed('Email is not verified.')

    return {
      'email': user.email,
      'username': user.username,
      'tokens': user.tokens
    }


class LogoutSerializer(serializers.Serializer):
  refresh = serializers.CharField()
  
  default_error_messages = {
    'bad_token': ('Token expired or  invalid'),
  }
  
  def validate(self, attrs):
    self.token = attrs['refresh']
    return attrs
  
  def save(self, **kwargs):
    try:
      RefreshToken(self.token).blacklist()
    except TokenError as identifier:
      self.fail('bad_token')  
  
  
class PasswordResetSerializer(serializers.Serializer):
  email = serializers.EmailField(min_length=2)
  redirect_url = serializers.CharField(min_length=0, max_length=50, required=False)
  
  class Meta:
    fields = ['email']
  

class SetNewPasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True)
  uidb64 = serializers.CharField(min_length=1, write_only=True)
  token = serializers.CharField(min_length=1, write_only=True)

  class Meta:
    fields = ['password', 'token', 'uidb64']
    
  def validate(self, attrs):
    try:
      password = attrs.get('password')
      uidb64 = attrs.get('uidb64')
      token = attrs.get('token')
      
      id = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=id)
      
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise AuthenticationFailed('The reset link is invalid.', 401)
      
      user.set_password(password)
      user.save()
      return user
    except Exception as e:
      raise AuthenticationFailed('The reset link is invalid.', 401) 
  