import jwt
from decouple import config
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User
from .renderers import UserRenderer
from .serializers import (EmailVerificationSerializer, LoginSerializer,
                          LogoutSerializer, PasswordResetSerializer,
                          RegisterSerializer, SetNewPasswordSerializer)
from .utils import Util
from django.views.generic import TemplateView


class GoogleView(TemplateView):
  permission_classes = []
  template_name = 'google.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["redirect_uri"] = "{}://{}".format(
      settings.SOCIAL_AUTH_PROTOCOL, settings.SOCIAL_AUTH_DOMAIN) 
    context["success_redirect_uri"] = "{}://{}".format(
      settings.PASSWORD_RESET_PROTOCOL, settings.PASSWORD_RESET_DOMAIN) 
    return context 
  
  
class CustomRedirect(HttpResponsePermanentRedirect):
  
  allowed_schemes = [config('APP_SCHEME'), 'http', 'https']
  
  
class RegisterView(GenericAPIView):
  serializer_class = RegisterSerializer
  renderer_classes = (UserRenderer, )
  
  @swagger_auto_schema(
    operation_summary='Register user',
    operation_description='This endpoint registers the user.',
    request_body=RegisterSerializer,
    # manual_parameters=[
    #   openapi.Parameter(
    #     "email",
    #     in_=openapi.IN_BODY,
    #     description="Email",
    #     type=openapi.TYPE_STRING
    #   ),
    #   openapi.Parameter(
    #     "password",
    #     in_=openapi.IN_BODY,
    #     description="Password",
    #     type=openapi.TYPE_STRING
    #   ),
    # ],
    responses={
      201: openapi.Response(
        description="User created successful",
        examples={
          "application/json": {
            "email": "email@gmail.com",
            "username": "username",
          },
        }
      ),
      400: openapi.Response(
        description="Error during registration",
        examples={
          "application/json": {
            "username": [
                "user with this username already exists."
            ],
            "email": [
                "user with this email already exists."
            ]   
          },
        },
      ),
    }
  )
  def post(self, request):
    user = request.data
    serializer = self.serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # created user
    user_data = serializer.data
    
    user = User.objects.get(email=user_data['email'])
    
    token = RefreshToken.for_user(user).access_token
    
    current_domain = get_current_site(request).domain
    relativeLink = reverse('verify-email')
    
    absolute_url = 'http://' + current_domain + relativeLink + "?token=" + str(token)
    email_body = 'Hi ' + user.username + '! ' + 'Click this link to verify your email \n' + absolute_url
    data = {
      'email_body': email_body,
      'email_subject': 'Verify your email',
      'to_email': user.email,
    }
    Util.send_email(data)
    
    return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
  serializer_class = EmailVerificationSerializer
  
  token_param_config = openapi.Parameter(
    "token",
    in_=openapi.IN_QUERY,
    description="Verification token",
    type=openapi.TYPE_STRING
  )
  responses = {
    200: openapi.Response(
      description="Verify email successful",
      examples={
        "application/json": {"email": "Email successfully activated."},
        "application/json": {"email": "Email has already been verified."},
      }
    ),
    400: openapi.Response(
      description="Error during email verification",
      examples={
          "application/json": {"error": "Activation link expired or Invalid token."},
          "application/json": {"error": "Invalid token."},
      },
    ),
  }
  
  @swagger_auto_schema(
    operation_summary='Verify Email',
    operation_description='This endpoint verifies the email.',
    manual_parameters=[token_param_config],
    responses=responses
  )
  def get(self, request):
    token = request.GET.get('token')
    # print("token: ", token)
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      # print("payload :", payload)
      user = User.objects.get(id=payload['user_id'])
      # print("user :", user)
      
      if not user.is_verified:
        user.is_verified = True
        user.save()
        return Response({ 'email': 'Email successfully activated.'}, status=status.HTTP_200_OK)
      else:
        return Response({'email': 'Email has already been verified.'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
      return Response({ 'error' : 'Activation link expired.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
      return Response({ 'error' : 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
 
    
class LoginView(GenericAPIView):
  serializer_class = LoginSerializer
  
  @swagger_auto_schema(
    operation_summary='Login user',
    operation_description='This endpoint logs in the user.',
    request_body=LoginSerializer,
    # manual_parameters=[
    #   openapi.Parameter(
    #     "email",
    #     in_=openapi.IN_BODY,
    #     description="Email",
    #     type=openapi.TYPE_STRING
    #   ),
    #   openapi.Parameter(
    #     "password",
    #     in_=openapi.IN_BODY,
    #     description="Password",
    #     type=openapi.TYPE_STRING
    #   ),
    # ],
    responses={
      200: openapi.Response(
        description="Login successful",
        examples={
          "application/json": {
            "email": "email@gmail.com",
            "username": "username",
            "tokens": "{'refresh': 'eyJ0eXAiOi', 'access': 'eyJ0b2kZ6r3o'}"
          },
        }
      ),
      400: openapi.Response(
        description="Error during login",
        examples={
            "application/json": {"detail": "Account disabled, contact admin."},
            "application/json": {"detail": "Email is not verified."},
            "application/json": {"detail": "Invalid credentials."},
        },
      ),
    }
  )
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


# def home(request):
#   return render(request, "home.html")

class LogoutView(GenericAPIView):
  serializer_class = LogoutSerializer
  permission_classes = (IsAuthenticated,)
  
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetView(GenericAPIView):
  serializer_class = PasswordResetSerializer
  
  def post(self, request):
    # data = { 'request': request, 'data': request.data}
    serializer = self.serializer_class(data=request.data)
    # serializer.is_valid(raise_exception=True)
    
    email = request.data['email']
    
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      
      current_domain = get_current_site(request).domain
      # current_domain = get_current_site(request=attrs['data'].get('request')).domain
      relativeLink = reverse('confirm-password-reset', kwargs={'uidb64': uidb64, 'token': token})
      redirect_url = request.data.get('redirect_url', '')
      absolute_url = 'http://' + current_domain + relativeLink
      
      email_body = 'Hello, \nUse this link to reset your password \n' + absolute_url + "?redirect_url=" + redirect_url
      data = {
        'email_body': email_body,
        'email_subject': 'Reset your password',
        'to_email': user.email,
      }
      Util.send_email(data)
    
    return Response({'success': ' A reset link has been sent to your email.'}, status=status.HTTP_200_OK)
   
    
class PasswordTokenCheckView(GenericAPIView):
  serializer_class = SetNewPasswordSerializer
  
  def get(self, request, uidb64, token):
    
    redirect_url = request.GET.get('redirect_url')
    
    try:
      id = smart_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=id)
  
      if not PasswordResetTokenGenerator().check_token(user, token):
        # return Response(
        #   {'error': "Token is not valid. Please request a new one."},
        #   status=status.HTTP_401_UNAUTHORIZED
        # )
        if len(redirect_url) > 3:
          return CustomRedirect(redirect_url+'?token_valid=False')
        else:
          return CustomRedirect(config('FRONTEND_URL', '') +'?token_valid=False')
       
      if redirect_url and len(redirect_url) > 3:   
        # return Response
        #   {'success': True, "message": "credentials valid", "uidb64": uidb64, 'token': token},
        #   status=status.HTTP_200_OK
        # )
        return CustomRedirect(
          redirect_url +
          '?token_valid=True&?message=Credentials valid&?uidb64=' +
          uidb64 +
          '&?token=' +
          token
        )
      else:
        return CustomRedirect(
          config('FRONTEND_URL', '') +
          '?token_valid=True&?message=Credentials valid&?uidb64=' +
          uidb64 +
          '&?token=' +
          token
        )
        
    except DjangoUnicodeDecodeError as identifier:
      # return Response(
      #   {'error': "Token is not valid. Please request a new one."},
      #   status=status.HTTP_401_UNAUTHORIZED
      # )
      return CustomRedirect(redirect_url+'?token_valid=False')
    
    
class SetNewPasswordView(GenericAPIView):
  serializer_class = SetNewPasswordSerializer
  
  def patch(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(
      {'success': True, 'message': 'Password reset successful.'},
      status=status.HTTP_200_OK
    )
