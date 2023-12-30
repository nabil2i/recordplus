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

User = auth.get_user_model()

# WITH DJOSER
class UserCreateSerializer(UserCreateSerializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True)
  
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = [ 'username', 'email', 'password']
    


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
    user = auth.authenticate(email=email, password=password)
    
    if filtered_user.exists() and filtered_user[0].auth_provider != 'email':
      raise AuthenticationFailed(detail="Please Login using " + filtered_user[0].auth_provider)
    
    ## debugging
    # import pdb
    # pdb.set_trace()
    
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


class PasswordResetSerializer(serializers.Serializer):
  email = serializers.EmailField(min_length=2)
  
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    
    email = attrs['data'].get('email', '')
    # user = User.objects.filter(email=email)
    # if user.exists():
    #   uidb64 = urlsafe_base64_encode(user.id)
    #   token = PasswordResetTokenGenerator().make_token(user)
      
    #   current_domain = get_current_site(attrs['request']).domain
    #   # current_domain = get_current_site(request=attrs['data'].get('request')).domain
    #   relativeLink = reverse('confirm-password-reset', kwargs={'uidb64': uidb64, 'token': token})
      
    #   absolute_url = 'http://' + current_domain + relativeLink
    #   email_body = 'Hello, \n User this link to reset your password \n' + absolute_url
    #   data = {
    #     'email_body': email_body,
    #     'email_subject': 'Reset your password',
    #     'to_email': user.email,
    #   }
    #   Util.send_email(data)
      
    return super().validate(attrs)
  

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
         
    return super().validate(attrs)
  