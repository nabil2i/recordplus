from django.shortcuts import render, redirect
from django.contrib.auth import logout
import jwt
from rest_framework.generics import GenericAPIView

from .renderers import UserRenderer
from .serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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


class VerifyEmail(APIView):
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

def logout_view(request):
  logout(request)
  return redirect("/api/auth")
